#!/usr/bin/env python3
"""Extract Hyprland key bindings from every source snapshot.

4.x ships default/hypr/bindings/*.lua using the Omarchy `o.bind(...)` helper.
3.x ships default/hypr/bindings/*.conf using Hyprland's own `bind*=` lines.
Both are normalised into the same record shape.

Writes data/bindings/<tag>.json and data/bindings/index.json.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import (  # noqa: E402
    DATA_DIR,
    available_tags,
    is_prerelease,
    read_text,
    source_url,
    tag_dir,
    write_json,
)

OUT_DIR = DATA_DIR / "bindings"

BIND_FUNCS = ("bind", "bind_toggle", "rebind", "unbind")

MODIFIERS = {
    "SUPER", "SHIFT", "CTRL", "CONTROL", "ALT", "MOD", "WIN", "LOGO", "CAPS",
    "MOD1", "MOD2", "MOD3", "MOD4", "MOD5",
}

CODE, STRING, COMMENT = "c", "s", "m"


# --------------------------------------------------------------------------
# Lua lexical scanning
# --------------------------------------------------------------------------

def _long_bracket_len(text: str, i: int) -> int | None:
    """If text[i:] opens a Lua long bracket, return the opener length."""
    if text[i] != "[":
        return None
    j = i + 1
    while j < len(text) and text[j] == "=":
        j += 1
    if j < len(text) and text[j] == "[":
        return j - i + 1
    return None


def lex_mask(text: str) -> str:
    """Classify every character as code, string, or comment."""
    n = len(text)
    mask = [CODE] * n
    i = 0
    while i < n:
        ch = text[i]

        if ch == "-" and text.startswith("--", i):
            opener = _long_bracket_len(text, i + 2)
            if opener:
                level = opener - 2
                close = "]" + "=" * level + "]"
                end = text.find(close, i + 2 + opener)
                end = n if end == -1 else end + len(close)
            else:
                end = text.find("\n", i)
                end = n if end == -1 else end
            for k in range(i, end):
                mask[k] = COMMENT
            i = end
            continue

        if ch in "\"'":
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == ch:
                    j += 1
                    break
                if text[j] == "\n":
                    break
                j += 1
            for k in range(i, min(j, n)):
                mask[k] = STRING
            i = j
            continue

        opener = _long_bracket_len(text, i)
        if opener:
            level = opener - 2
            close = "]" + "=" * level + "]"
            end = text.find(close, i + opener)
            end = n if end == -1 else end + len(close)
            for k in range(i, end):
                mask[k] = STRING
            i = end
            continue

        i += 1

    return "".join(mask)


def code_only(text: str, mask: str) -> str:
    """Same length as text, with strings and comments blanked out."""
    return "".join(c if m == CODE else (" " if c != "\n" else "\n")
                   for c, m in zip(text, mask))


# --------------------------------------------------------------------------
# Lua expression evaluation (only the trivially-static subset)
# --------------------------------------------------------------------------

class NotStatic(Exception):
    pass


LUA_ESCAPES = {
    "a": "\a", "b": "\b", "f": "\f", "n": "\n", "r": "\r",
    "t": "\t", "v": "\v", "\\": "\\", '"': '"', "'": "'", "\n": "\n",
}


def lua_unquote(literal: str) -> str:
    """Decode a Lua short-string literal, honouring escape sequences."""
    quote = literal[0]
    body = literal[1:-1] if literal.endswith(quote) and len(literal) > 1 else literal[1:]
    out = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(body):
            break
        esc = body[i]
        if esc in LUA_ESCAPES:
            out.append(LUA_ESCAPES[esc])
            i += 1
        elif esc == "x":
            out.append(chr(int(body[i + 1:i + 3], 16)))
            i += 3
        elif esc == "z":
            i += 1
            while i < len(body) and body[i].isspace():
                i += 1
        elif esc.isdigit():
            j = i
            while j < len(body) and j < i + 3 and body[j].isdigit():
                j += 1
            out.append(chr(int(body[i:j])))
            i = j
        else:
            out.append(esc)
            i += 1
    return "".join(out)


TOKEN_RE = re.compile(
    r"""\s*(?:
        (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
      | (?P<number>\d+(?:\.\d+)?)
      | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
      | (?P<concat>\.\.)
      | (?P<op>[()+\-*/,])
    )""",
    re.X,
)


def _tokenize(expr: str):
    pos = 0
    out = []
    while pos < len(expr):
        m = TOKEN_RE.match(expr, pos)
        if not m:
            if expr[pos:].strip() == "":
                break
            raise NotStatic(expr)
        pos = m.end()
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
    return out


def lua_eval(expr: str, env: dict):
    """Evaluate the static subset: literals, env names, arithmetic, `..`, tostring()."""
    expr = expr.strip()
    if not expr:
        raise NotStatic(expr)
    tokens = _tokenize(expr)
    if not tokens:
        raise NotStatic(expr)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else (None, None)

    def take():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def primary():
        nonlocal pos
        kind, val = peek()
        if kind is None:
            raise NotStatic(expr)
        if kind == "string":
            take()
            return lua_unquote(val)
        if kind == "number":
            take()
            return int(val) if "." not in val else float(val)
        if kind == "name":
            take()
            if peek() == ("op", "("):
                if val != "tostring":
                    raise NotStatic(expr)
                take()
                inner = concat()
                if peek() != ("op", ")"):
                    raise NotStatic(expr)
                take()
                return tostring(inner)
            if val in env:
                return env[val]
            raise NotStatic(expr)
        if kind == "op" and val == "(":
            take()
            inner = concat()
            if peek() != ("op", ")"):
                raise NotStatic(expr)
            take()
            return inner
        if kind == "op" and val == "-":
            take()
            return -primary()
        raise NotStatic(expr)

    def product():
        left = primary()
        while peek()[0] == "op" and peek()[1] in "*/":
            _, op = take()
            right = primary()
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise NotStatic(expr)
            left = left * right if op == "*" else left / right
        return left

    def arith():
        left = product()
        while peek()[0] == "op" and peek()[1] in "+-":
            _, op = take()
            right = product()
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise NotStatic(expr)
            left = left + right if op == "+" else left - right
        return left

    def concat():
        left = arith()
        while peek()[0] == "concat":
            take()
            right = arith()
            left = tostring(left) + tostring(right)
        return left

    value = concat()
    if pos != len(tokens):
        raise NotStatic(expr)
    return value


def tostring(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else str(value)
    if isinstance(value, str):
        return value
    raise NotStatic(repr(value))


# --------------------------------------------------------------------------
# Lua bindings file parsing
# --------------------------------------------------------------------------

OPENERS = {"do", "then", "function", "repeat"}
CLOSERS = {"end", "until"}
WORD_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")

NUMERIC_FOR_RE = re.compile(
    r"\bfor\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+)\s*,\s*(-?\d+)\s*"
    r"(?:,\s*(-?\d+)\s*)?\bdo\b"
)
LOCAL_ASSIGN_RE = re.compile(r"^[ \t]*local[ \t]+([A-Za-z_][A-Za-z0-9_]*)[ \t]*=(.*)$", re.M)


def block_end(code: str, start: int) -> int:
    """Index just past the `end` that closes a block opened at/just before `start`."""
    depth = 1
    for m in WORD_RE.finditer(code, start):
        word = m.group(0)
        if word == "elseif":
            depth -= 1
        elif word in OPENERS:
            depth += 1
        elif word in CLOSERS:
            depth -= 1
            if depth == 0:
                return m.end()
    return len(code)


def match_paren(code: str, open_idx: int) -> int:
    """Index of the `)` matching the `(` at open_idx (code-only text)."""
    depth = 0
    for i in range(open_idx, len(code)):
        ch = code[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def split_args(code: str, text: str, start: int, end: int) -> list[tuple[int, int]]:
    """Top-level comma split of text[start:end]; returns (from, to) offsets."""
    spans = []
    depth = 0
    cur = start
    for i in range(start, end):
        ch = code[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            spans.append((cur, i))
            cur = i + 1
    spans.append((cur, end))
    return [(a, b) for a, b in spans if text[a:b].strip()]


def normalise_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def chord_keys(chord: str) -> list[str]:
    parts = [p.strip() for p in chord.split("+") if p.strip()]
    return [p.upper() if p.upper() in MODIFIERS else p for p in parts]


def parse_lua_file(tag: str, path, relpath: str) -> list[dict]:
    text = read_text(path)
    mask = lex_mask(text)
    code = code_only(text, mask)

    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    def line_of(idx: int) -> int:
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= idx:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    # Numeric for-loops: (body_start, body_end, var, values)
    loops = []
    for m in NUMERIC_FOR_RE.finditer(code):
        start, stop = int(m.group(2)), int(m.group(3))
        step = int(m.group(4)) if m.group(4) else 1
        if step == 0:
            continue
        values = list(range(start, stop + 1, step)) if step > 0 else list(range(start, stop - 1, step))
        loops.append((m.end(), block_end(code, m.end()), m.group(1), values))

    records: list[dict] = []
    call_re = re.compile(r"\bo\.(" + "|".join(BIND_FUNCS) + r")\s*\(")

    for m in call_re.finditer(code):
        kind = m.group(1)
        open_idx = code.index("(", m.end() - 1)
        close_idx = match_paren(code, open_idx)
        if close_idx == -1:
            continue
        spans = split_args(code, text, open_idx + 1, close_idx)
        if not spans:
            continue

        raw = [text[a:b].strip() for a, b in spans]
        line = line_of(m.start())

        enclosing = [lp for lp in loops if lp[0] <= m.start() < lp[1]]

        # Environment candidates: one dict per iteration of the enclosing loops.
        envs: list[dict] = [{}]
        for body_start, body_end, var, values in enclosing:
            # Locate assignments in the code view (so strings and comments cannot
            # produce false matches), then read the expression from the real text.
            assigns = []
            for am in LOCAL_ASSIGN_RE.finditer(code[body_start:body_end]):
                at = body_start + am.start()
                if at >= m.start():
                    continue
                expr = text[body_start + am.start(2):body_start + am.end(2)].strip()
                assigns.append((at, am.group(1), expr))
            expanded = []
            for env in envs:
                for value in values:
                    child = dict(env)
                    child[var] = value
                    for _, name, expr in assigns:
                        try:
                            child[name] = lua_eval(expr, child)
                        except NotStatic:
                            pass
                    expanded.append(child)
            envs = expanded

        note = None
        if enclosing:
            descr = ", ".join(
                f"{var} = {values[0]}-{values[-1]}" for _, _, var, values in enclosing
            )
            note = f"generated: {descr}"

        emitted = 0
        for env in envs:
            try:
                chord = lua_eval(raw[0], env)
                if not isinstance(chord, str):
                    raise NotStatic(raw[0])
            except NotStatic:
                chord = None

            label = None
            if len(raw) > 1 and raw[1] != "nil":
                try:
                    value = lua_eval(raw[1], env)
                    label = value if isinstance(value, str) else tostring(value)
                except NotStatic:
                    label = None

            action = None
            if len(raw) > 2:
                try:
                    value = lua_eval(raw[2], env)
                    action = value if isinstance(value, str) else tostring(value)
                except NotStatic:
                    action = normalise_ws(raw[2])

            record_note = note
            if chord is None:
                chord = normalise_ws(raw[0])
                record_note = (note + "; " if note else "") + "unexpanded: dynamic chord"

            records.append({
                "action": action,
                "category": path.stem,
                "chord": chord,
                "file": relpath,
                "keys": chord_keys(chord),
                "kind": kind,
                "label": label,
                "line": line,
                "note": record_note,
                "options": normalise_ws(raw[3]) if len(raw) > 3 else None,
                "sourceUrl": f"{source_url(tag, relpath)}#L{line}",
            })
            emitted += 1
            if chord is None:
                break

        if emitted == 0:
            continue

    return records


# --------------------------------------------------------------------------
# Hyprland .conf bindings parsing (3.x)
# --------------------------------------------------------------------------

CONF_BIND_RE = re.compile(r"^[ \t]*(bind[a-z]*)[ \t]*=[ \t]*(.*)$")


def best_effort_label(dispatcher: str, params: str) -> str:
    """Derive a readable label when the bind carries no description flag."""
    if dispatcher == "exec":
        command = params.strip().split("&&")[0].split("||")[0].strip()
        binary = command.split()[0] if command.split() else command
        binary = binary.rsplit("/", 1)[-1]
        if binary.startswith("omarchy-"):
            binary = binary[len("omarchy-"):]
        words = binary.replace("-", " ").replace("_", " ").strip()
        return words[:1].upper() + words[1:] if words else command
    text = " ".join(x for x in (dispatcher, params.strip()) if x)
    return text[:1].upper() + text[1:] if text else dispatcher


def parse_conf_file(tag: str, path, relpath: str) -> list[dict]:
    records = []
    for lineno, raw_line in enumerate(read_text(path).splitlines(), start=1):
        m = CONF_BIND_RE.match(raw_line)
        if not m:
            continue
        kind, value = m.group(1), m.group(2)
        # Hyprland treats '#' as a comment anywhere on the line.
        if "#" in value:
            value = value.split("#", 1)[0]
        value = value.rstrip()
        if not value:
            continue

        flags = kind[len("bind"):]
        has_description = "d" in flags
        field_count = 5 if has_description else 4
        fields = [f.strip() for f in value.split(",", field_count - 1)]
        while len(fields) < field_count:
            fields.append("")

        if has_description:
            mods, key, label, dispatcher, params = fields[:5]
        else:
            mods, key, dispatcher, params = fields[:4]
            label = ""

        params = params.rstrip().rstrip(",").strip()
        mod_parts = [p for p in mods.replace("+", " ").split() if p]
        chord = " + ".join(mod_parts + ([key] if key else []))

        if dispatcher == "exec":
            action = params
        else:
            action = " ".join(x for x in (dispatcher, params) if x).strip()

        records.append({
            "action": action,
            "category": path.stem,
            "chord": chord,
            "file": relpath,
            "keys": chord_keys(chord),
            "kind": kind,
            "label": label or best_effort_label(dispatcher, params),
            "line": lineno,
            "note": None if has_description else "label derived from the command (bind has no description flag)",
            "options": None,
            "sourceUrl": f"{source_url(tag, relpath)}#L{lineno}",
        })
    return records


# --------------------------------------------------------------------------

def process_tag(tag: str) -> dict:
    bindings_dir = tag_dir(tag) / "default" / "hypr" / "bindings"
    records: list[dict] = []
    fmt = None

    if bindings_dir.is_dir():
        lua_files = sorted(bindings_dir.glob("*.lua"))
        conf_files = sorted(bindings_dir.glob("*.conf"))
        if lua_files:
            fmt = "lua"
            for path in lua_files:
                records += parse_lua_file(tag, path, f"default/hypr/bindings/{path.name}")
        elif conf_files:
            fmt = "conf"
            for path in conf_files:
                records += parse_conf_file(tag, path, f"default/hypr/bindings/{path.name}")

    records.sort(key=lambda r: (r["file"], r["line"], r["chord"]))

    payload = {
        "bindings": records,
        "count": len(records),
        "format": fmt,
        "generatedFrom": f"data/source/{tag}/default/hypr/bindings",
        "prerelease": is_prerelease(tag),
        "tag": tag,
    }
    write_json(OUT_DIR / f"{tag}.json", payload)
    return payload


def main() -> int:
    tags = available_tags()
    if not tags:
        print("no snapshots under data/source/", file=sys.stderr)
        return 1

    counts = {}
    for tag in tags:
        payload = process_tag(tag)
        recs = payload["bindings"]
        counts[tag] = {
            "bindings": len(recs),
            "categories": len({r["category"] for r in recs}),
            "format": payload["format"],
            "generated": sum(1 for r in recs if r["note"] and r["note"].startswith("generated")),
        }
        print(
            f"  bindings {tag:<12} {counts[tag]['bindings']:>4} bindings "
            f"({payload['format']}), {counts[tag]['generated']:>3} loop-generated"
        )

    write_json(OUT_DIR / "index.json", {"counts": counts, "tags": tags})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

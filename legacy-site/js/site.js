(function () {
  var data = (window.HARDWARE || []).slice();
  var RANK = { gold: 0, silver: 1, bronze: 2, experimental: 3, broken: 4 };
  data.sort(function (a, b) {
    var r = (RANK[a.rating] || 9) - (RANK[b.rating] || 9);
    return r !== 0 ? r : a.name.localeCompare(b.name);
  });

  var q = document.getElementById("q");
  var pills = document.getElementById("pills");
  var brandsEl = document.getElementById("brands");
  var typesEl = document.getElementById("types");
  var results = document.getElementById("results");
  var empty = document.getElementById("empty");
  var tally = document.getElementById("tally");
  if (!results && !document.getElementById("matrix")) return;

  var rating = "all";
  var brand = "all";
  var type = "all";

  function hay(m) {
    return [m.name, m.summary, m.type, m.brand, m.tags, m.id].join(" ").toLowerCase();
  }

  function filtered() {
    var needle = (q && q.value ? q.value : "").toLowerCase().trim();
    return data.filter(function (m) {
      if (rating !== "all" && m.rating !== rating) return false;
      if (brand !== "all" && m.brand !== brand) return false;
      if (type !== "all" && m.type !== type) return false;
      if (needle && hay(m).indexOf(needle) === -1) return false;
      return true;
    });
  }

  function label(v) {
    if (v === "works") return '<span class="dot works">works</span>';
    if (v === "workaround") return '<span class="dot workaround">workaround</span>';
    if (v === "fails" || v === "no") return '<span class="dot fails">fails</span>';
    if (v === "n/a") return '<span class="dot unknown">n/a</span>';
    return '<span class="dot unknown">unknown</span>';
  }

  function render() {
    var rows = filtered();
    if (tally) {
      tally.textContent = rows.length + " of " + data.length + " machines";
    }
    if (results) {
      results.innerHTML = rows
        .map(function (m) {
          var inHardware = !!document.getElementById("matrix") || /\/hardware(\/|$)/.test(location.pathname);
          var href = m.href.indexOf("http") === 0 ? m.href : inHardware ? m.href : "hardware/" + m.href;
          return (
            '<a class="card" href="' +
            href +
            '"><span class="badge ' +
            m.rating +
            '">' +
            m.rating +
            "</span><h3>" +
            m.name +
            "</h3><p>" +
            m.summary +
            "</p></a>"
          );
        })
        .join("");
    }
    if (empty) empty.hidden = rows.length > 0;
    var table = document.getElementById("matrix");
    if (table) {
      table.querySelector("tbody").innerHTML = rows
        .map(function (m) {
          return (
            "<tr><td><a href=\"" +
            m.href +
            "\">" +
            m.name +
            "</a></td><td>" +
            (m.brand || "") +
            '</td><td><span class="badge ' +
            m.rating +
            '">' +
            m.rating +
            "</span></td><td>" +
            label(m.wifi) +
            "</td><td>" +
            label(m.audio) +
            "</td><td>" +
            label(m.webcam) +
            "</td><td>" +
            label(m.fingerprint) +
            "</td><td>" +
            label(m.gpu) +
            "</td><td>" +
            label(m.suspend) +
            "</td></tr>"
          );
        })
        .join("");
    }
  }

  function bindPills(el, key) {
    if (!el) return;
    el.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (key === "rating") rating = b.getAttribute("data-rating");
      if (key === "brand") brand = b.getAttribute("data-brand");
      if (key === "type") type = b.getAttribute("data-type");
      Array.prototype.forEach.call(el.querySelectorAll("button"), function (x) {
        x.classList.toggle("on", x === b);
      });
      render();
    });
  }

  if (brandsEl) {
    var brands = [];
    data.forEach(function (m) {
      if (m.brand && brands.indexOf(m.brand) === -1) brands.push(m.brand);
    });
    brands.sort();
    brandsEl.innerHTML =
      '<button type="button" class="on" data-brand="all">All</button>' +
      brands
        .map(function (b) {
          return '<button type="button" data-brand="' + b + '">' + b + "</button>";
        })
        .join("");
  }

  if (q) {
    var params = new URLSearchParams(location.search);
    if (params.get("q") && !q.value) q.value = params.get("q");
    q.addEventListener("input", render);
  }
  bindPills(pills, "rating");
  bindPills(brandsEl, "brand");
  bindPills(typesEl, "type");
  render();
})();

/* Statistik dampak (count-up) + peta area kerja MDI. Tanpa inline script (kompatibel CSP). */
(function () {
  "use strict";
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- count-up ---- */
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target) || reduced) { return; }
    var dur = 1200, start = null;
    el.textContent = "0";
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString();
      if (p < 1) requestAnimationFrame(step); else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  }
  var nums = Array.prototype.slice.call(document.querySelectorAll("[data-count]"));
  if (nums.length) {
    if ("IntersectionObserver" in window && !reduced) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); io.unobserve(e.target); } });
      }, { threshold: 0.4 });
      nums.forEach(function (n) { io.observe(n); });
    }
  }

  /* ---- peta area kerja ---- */
  var mapEl = document.getElementById("mdiImpactMap");
  if (!mapEl || typeof L === "undefined") return;
  var dataEl = document.getElementById(mapEl.getAttribute("data-points-id"));
  var points = [];
  try { points = JSON.parse(dataEl.textContent) || []; } catch (e) { return; }
  if (!points.length) return;

  var map = L.map(mapEl, { scrollWheelZoom: false, tap: true }).setView([-8.8, 125.7], 8);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 14,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
  }).addTo(map);
  map.on("focus", function () { map.scrollWheelZoom.enable(); });
  map.on("blur", function () { map.scrollWheelZoom.disable(); });

  var max = Math.max.apply(null, points.map(function (p) { return p.count; }));
  var bounds = [];
  points.forEach(function (p) {
    var radius = 10 + 18 * Math.sqrt(p.count / max);
    var m = L.circleMarker([p.lat, p.lng], {
      radius: radius, color: "#7C141C", weight: 2, fillColor: "#A11D26", fillOpacity: 0.55
    }).addTo(map);
    var box = document.createElement("div");
    var b = document.createElement("strong"); b.textContent = p.name; box.appendChild(b);
    box.appendChild(document.createElement("br"));
    box.appendChild(document.createTextNode(p.count + " " + (mapEl.getAttribute("data-unit") || "")));
    box.appendChild(document.createElement("br"));
    var a = document.createElement("a");
    a.href = "/what-we-do/?mun=" + encodeURIComponent(p.name);
    a.textContent = mapEl.getAttribute("data-more") || "View";
    box.appendChild(a);
    m.bindPopup(box);
    bounds.push([p.lat, p.lng]);
  });
  if (bounds.length > 1) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 9 });
  else map.setView(bounds[0], 10);
})();

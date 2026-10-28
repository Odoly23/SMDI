/* Muat Leaflet (144 KB) hanya saat peta mendekati layar, dan library rute (819 KB) hanya saat tombol "Rute" diklik.
   Tanpa ini beranda memuat ~1 MB JavaScript yang mungkin tak pernah dipakai pengunjung. */
(function () {
  "use strict";
  var cfg = document.currentScript ? document.currentScript.dataset : {};
  window.MDI = window.MDI || {};
  var cache = {};

  function loadScript(src) {
    if (!src) return Promise.reject(new Error("no src"));
    if (!cache[src]) {
      cache[src] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = src; s.async = true;
        s.onload = resolve; s.onerror = function () { delete cache[src]; reject(new Error("load " + src)); };
        document.head.appendChild(s);
      });
    }
    return cache[src];
  }

  window.MDI.loadRouting = function () {
    return loadScript(cfg.leaflet).then(function () { return loadScript(cfg.routing); });
  };

  var targets = [
    { id: "mdiLeafletMap", init: function () { return loadScript(cfg.leaflet).then(function () { return loadScript(cfg.homeMap); }).then(function () { window.MDI.initHomeMap(); }); } },
    { id: "mdiImpactMap", init: function () { return loadScript(cfg.leaflet).then(function () { window.MDI.initImpactMap(); }); } }
  ];

  targets.forEach(function (t) {
    var el = document.getElementById(t.id);
    if (!el) return;
    var started = false;
    function go() { if (started) return; started = true; t.init().catch(function () {}); }
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); go(); }
      }, { rootMargin: "400px 0px" });
      io.observe(el);
    } else { go(); }
  });
})();

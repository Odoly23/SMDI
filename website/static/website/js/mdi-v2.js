/* MDI: JavaScript kecil, tanpa dependensi. Semua fitur punya fallback tanpa JS. */
(function () {
  "use strict";

  /* 0. AOS: fade saat scroll. Mati otomatis bila pengguna memilih "kurangi gerakan" atau AOS gagal dimuat,
        sehingga konten tidak pernah tersembunyi. */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (window.AOS && !reduce) {
    window.AOS.init({ duration: 800, easing: "ease-out-cubic", once: true, offset: 70 });
  } else {
    document.querySelectorAll("[data-aos]").forEach(function (el) { el.removeAttribute("data-aos"); });
  }

  /* slider: tanpa gerak otomatis bila pengguna memilih "kurangi gerakan" */
  var hero = document.getElementById("mdiHero");
  if (hero && reduce && window.bootstrap) {
    window.bootstrap.Carousel.getOrCreateInstance(hero, { ride: false, interval: false }).pause();
  }

  /* 0b. Navbar: bayangan halus setelah scroll (respons atas aksi pengguna) */
  var nav = document.querySelector(".mdi-nav");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("is-scrolled", window.scrollY > 12); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* 1. Tinan servisu dihitung otomatis dari data-years-since (fallback teks "20+" bila JS mati) */
  document.querySelectorAll("[data-years-since]").forEach(function (el) {
    var since = parseInt(el.getAttribute("data-years-since"), 10);
    if (!isNaN(since)) el.textContent = String(new Date().getFullYear() - since);
  });

})();

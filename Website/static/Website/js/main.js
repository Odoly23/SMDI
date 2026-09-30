/* =========================================================
   MATA DALAN INSTITUTE — main.js
   - Database content translation (data-i18n-multi / data-i18n-list),
     paralelu ho Django's own {% trans %} static-text i18n system.
     Lian aktivu deriva husi <html lang="..."> (seteia husi Django
     set_language view + LocaleMiddleware, la uza localStorage tan).
   - Navbar Program submenu (hover iha desktop, accordion iha mobile)
   - Navbar active state, back-to-top, year stamp
   ========================================================= */
(function () {
  "use strict";

  var DEFAULT_LANG = "tet";

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* ---------- LANGUAGE (banco de dadus/JSON multi-lian) ---------- */
  function getLang() {
    var htmlLang = document.documentElement.getAttribute("lang");
    return htmlLang || DEFAULT_LANG;
  }

  function applyTranslations(lang) {
    // Teks curtu/dinámiku (Vision/Mission, Program, Slide, WhoWeAre, dst)
    qsa("[data-i18n-multi]").forEach(function (el) {
      try {
        var map = JSON.parse(el.getAttribute("data-i18n-multi"));
        var text = map[lang] || map[DEFAULT_LANG] || map.tet;
        if (text !== undefined) el.textContent = text;
      } catch (e) { /* abaikan JSON invalid, biar teks default tetap */ }
    });

    // Lista (mission_points, indicators, org_structure_items, geo_focus_regions)
    qsa("[data-i18n-list]").forEach(function (el) {
      try {
        var map = JSON.parse(el.getAttribute("data-i18n-list"));
        var items = map[lang] || map[DEFAULT_LANG] || map.tet;
        if (!items || !items.length) return;
        var tag = el.getAttribute("data-i18n-list-tag") || "li";
        var extraClass = el.getAttribute("data-i18n-list-class") || "";
        el.innerHTML = "";
        items.forEach(function (text) {
          var node = document.createElement(tag);
          if (extraClass) node.className = extraClass;
          if (tag === "li" && el.classList.contains("indicator-list")) {
            node.className = "indicator-item";
          }
          node.textContent = text;
          el.appendChild(node);
        });
      } catch (e) { /* abaikan JSON invalid */ }
    });
  }

  /* ---------- NAVBAR: PROGRAM SUBMENU (Pilar > Sub-Outcome) ---------- */
  function initSubmenus() {
    var isMobile = function () { return window.innerWidth < 992; };

    qsa(".dropdown-submenu > .dropdown-submenu-toggle").forEach(function (toggle) {
      toggle.addEventListener("click", function (e) {
        if (isMobile()) {
          // Iha mobile: klik primeiru habre/taka submenu (accordion), klik daruak bele navega
          var parent = toggle.closest(".dropdown-submenu");
          var submenu = parent.querySelector(".dropdown-submenu-menu");
          var alreadyOpen = parent.classList.contains("submenu-open");
          if (!alreadyOpen) {
            e.preventDefault();
            qsa(".dropdown-submenu.submenu-open", parent.parentElement).forEach(function (openParent) {
              if (openParent !== parent) openParent.classList.remove("submenu-open");
            });
            parent.classList.add("submenu-open");
          }
          // se ja open, husik link laran hala'o normalmente (navega ba program_detail)
        }
        // Iha desktop: hover trata submenu (CSS), klik iha label mesak navega ba pillar detail
      });
    });
  }

  /* ---------- NAVBAR ACTIVE LINK ---------- */
  function markActiveNav() {
    var path = window.location.pathname;
    qsa(".navbar-mdi .nav-link, .navbar-mdi .dropdown-item").forEach(function (link) {
      var href = link.getAttribute("href");
      if (href && href !== "#" && path === href) {
        link.classList.add("active");
        var parentDropdown = link.closest(".dropdown");
        if (parentDropdown) {
          var toggle = parentDropdown.querySelector(".nav-link.dropdown-toggle");
          if (toggle) toggle.classList.add("active");
        }
      }
    });
  }

  /* ---------- BACK TO TOP ---------- */
  function initBackToTop() {
    var btn = document.querySelector(".back-to-top");
    if (!btn) return;
    window.addEventListener("scroll", function () {
      btn.classList.toggle("show", window.scrollY > 400);
    });
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------- YEAR STAMP ---------- */
  function stampYear() {
    qsa("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyTranslations(getLang());
    initSubmenus();
    markActiveNav();
    initBackToTop();
    stampYear();
  });

  window.MDI = { getLang: getLang };
})();

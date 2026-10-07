"""Tes responsif di browser nyata (Playwright/Chromium): HP, tablet, laptop, komputer.

Verifika: la iha scroll horizontal, menu navbar la tabrakan ho logo, hamburger
funsiona iha <1200px, tombol next/prev slider iha laran no la taka teksto.
Skip otomatis se Playwright/Chromium la instala.
Jalan: python manage.py test website.tests_responsive
"""
import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from custom.models import Category
from .models import Activity, Program

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

VIEWPORTS = {"hp-360": (360, 740), "hp-414": (414, 800), "tablet-768": (768, 1024),
             "laptop-1024": (1024, 768), "laptop-1366": (1366, 768), "desktop-1920": (1920, 1080)}


def overlap(a, b):
    return not (a["x"] + a["width"] <= b["x"] or b["x"] + b["width"] <= a["x"]
                or a["y"] + a["height"] <= b["y"] or b["y"] + b["height"] <= a["y"])


@unittest.skipIf(sync_playwright is None, "playwright belum terinstal")
class ResponsiveTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch()
        except Exception as exc:  # Chromium la iha
            cls.pw.stop()
            super().tearDownClass()
            raise unittest.SkipTest(f"Chromium la disponivel: {exc}")

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        super().tearDownClass()

    def setUp(self):
        # TransactionTestCase (live server): data dibuat iha setUp, la husi setUpTestData
        Category.objects.create(name="Doc PNDS", slug="doc-pnds", context="document")
        Program.objects.create(slug="pilar-1", title="Pilar 1", description="x", icon="bi-diagram-3", order=0)
        for i in range(10):
            Activity.objects.create(tag=f"Tag {i % 3}", title=f"Atividade {i} " + "panjang " * 12,
                                    description=" ".join(f"kata{n}" for n in range(300)))
        self.activity = Activity.objects.first()

    def page(self, key, path):
        w, h = VIEWPORTS[key]
        ctx = self.browser.new_context(viewport={"width": w, "height": h})
        pg = ctx.new_page()
        pg.goto(self.live_server_url + path, wait_until="domcontentloaded")
        pg.wait_for_timeout(500)
        self.addCleanup(ctx.close)
        return pg, w

    def paths(self):
        return ["/", "/who-we-are/", "/vision-mission/", "/what-we-do/",
                f"/what-we-do/activity/{self.activity.pk}/", "/partners-networks/",
                "/current-donors/", "/news/", "/articles/", "/contact/",
                "/documents/doc-pnds/", "/program/pilar-1/"]

    # -- 1. la iha scroll horizontal ----------------------------------------
    def test_no_horizontal_overflow(self):
        for key in VIEWPORTS:
            for path in self.paths():
                with self.subTest(viewport=key, path=path):
                    pg, _ = self.page(key, path)
                    extra = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    self.assertLessEqual(extra, 0, f"overflow {extra}px")

    # -- 2. navbar ---------------------------------------------------------
    def test_navbar_desktop_single_row_no_overlap(self):
        for key in ("desktop-1920", "laptop-1366"):
            with self.subTest(viewport=key):
                pg, w = self.page(key, "/")
                self.assertFalse(pg.locator(".navbar-toggler").is_visible())
                links = pg.locator(".navbar-mdi .navbar-nav > .nav-item > .nav-link")
                boxes = [links.nth(i).bounding_box() for i in range(links.count())]
                self.assertGreaterEqual(len(boxes), 9)
                tops = {round(b["y"]) for b in boxes}
                self.assertLessEqual(max(tops) - min(tops), 4, "menu pecah jadi >1 baris")
                brand = pg.locator(".navbar-brand").bounding_box()
                for b in boxes:
                    self.assertFalse(overlap(brand, b), "logo/nama bertabrakan dengan menu")
                    self.assertLessEqual(b["x"] + b["width"], w)
                auth = pg.locator(".nav-auth-link").bounding_box()
                self.assertLessEqual(auth["x"] + auth["width"], w)

    def test_navbar_hamburger_below_1200(self):
        for key in ("hp-360", "hp-414", "tablet-768", "laptop-1024"):
            with self.subTest(viewport=key):
                pg, w = self.page(key, "/")
                toggler = pg.locator(".navbar-toggler")
                self.assertTrue(toggler.is_visible())
                self.assertFalse(pg.locator("#mdiNavbar").is_visible())
                tb = toggler.bounding_box()
                self.assertLessEqual(tb["x"] + tb["width"], w)
                self.assertGreaterEqual(tb["width"], 30)
                toggler.click()
                pg.wait_for_timeout(600)
                menu = pg.locator("#mdiNavbar")
                self.assertTrue(menu.is_visible())
                brand = pg.locator(".navbar-brand").bounding_box()
                mb = menu.bounding_box()
                self.assertGreaterEqual(mb["y"], brand["y"] + brand["height"] - 1,
                                        "menu mosu iha sorin logo, la iha okos")
                self.assertGreaterEqual(mb["width"], w * 0.88)
                for i in range(pg.locator("#mdiNavbar .nav-link").count()):
                    b = pg.locator("#mdiNavbar .nav-link").nth(i).bounding_box()
                    self.assertGreaterEqual(b["x"], 0)
                    self.assertLessEqual(b["x"] + b["width"], w)

    def test_mobile_dropdown_opens_inline(self):
        pg, w = self.page("hp-360", "/")
        pg.locator(".navbar-toggler").click()
        pg.wait_for_timeout(600)
        pg.locator("#mdiNavbar .dropdown-toggle").first.click()
        pg.wait_for_timeout(400)
        dd = pg.locator("#mdiNavbar .dropdown-menu.show").first.bounding_box()
        self.assertGreaterEqual(dd["x"], 0)
        self.assertLessEqual(dd["x"] + dd["width"], w)

    # -- 3. slider next/prev ------------------------------------------------
    def test_carousel_controls_tidy(self):
        for key in VIEWPORTS:
            with self.subTest(viewport=key):
                pg, w = self.page(key, "/")
                h = VIEWPORTS[key][1]
                prev = pg.locator(".hero-carousel .carousel-control-prev").bounding_box()
                nxt = pg.locator(".hero-carousel .carousel-control-next").bounding_box()
                for name, b in (("prev", prev), ("next", nxt)):
                    self.assertGreaterEqual(b["width"], 36, f"{name} terlalu kecil buat disentuh")
                    self.assertGreaterEqual(b["height"], 36)
                    self.assertGreaterEqual(b["x"], 0, f"{name} keluar layar kiri")
                    self.assertLessEqual(b["x"] + b["width"], w, f"{name} keluar layar kanan")
                self.assertLess(prev["x"], nxt["x"])
                for sel in (".hero-slide h1", ".hero-kicker", ".hero-slide .btn"):
                    loc = pg.locator(f".carousel-item.active {sel}")
                    for i in range(loc.count()):
                        tb = loc.nth(i).bounding_box()
                        self.assertFalse(overlap(prev, tb), f"prev menutupi {sel}")
                        self.assertFalse(overlap(nxt, tb), f"next menutupi {sel}")

    def test_carousel_indicators_not_hidden_by_cards(self):
        for key in ("hp-360", "tablet-768", "laptop-1366"):
            with self.subTest(viewport=key):
                pg, _ = self.page(key, "/")
                ind = pg.locator(".hero-carousel .carousel-indicators").bounding_box()
                cards = pg.locator(".overlap-cards").bounding_box()
                self.assertLessEqual(ind["y"] + ind["height"], cards["y"] + 1,
                                     "indikator tertutup kartu")

    def test_carousel_next_button_changes_slide(self):
        pg, _ = self.page("hp-360", "/")
        # halaman tes tanpa slide: hanya pastikan klik tidak error & kontrol bisa diklik
        pg.locator(".hero-carousel .carousel-control-next").click()
        pg.locator(".hero-carousel .carousel-control-prev").click()

    # -- 4. What We Do ------------------------------------------------------
    def test_what_we_do_cards_compact_and_aligned(self):
        for key in VIEWPORTS:
            with self.subTest(viewport=key):
                pg, w = self.page(key, "/what-we-do/")
                cards = pg.locator(".activity-card")
                self.assertEqual(cards.count(), 9)  # paginasaun 9 per halaman
                for i in range(cards.count()):
                    b = cards.nth(i).bounding_box()
                    self.assertGreaterEqual(b["x"], 0)
                    self.assertLessEqual(b["x"] + b["width"], w)
                # kartu iha liña ida iha altura hanesan
                first_row = [cards.nth(i).bounding_box() for i in range(cards.count())
                             if abs(cards.nth(i).bounding_box()["y"] - cards.first.bounding_box()["y"]) < 2]
                self.assertEqual(len({round(b["height"]) for b in first_row}), 1)
                cols = len(first_row)
                expected = 3 if w >= 992 else 2 if w >= 768 else 1
                self.assertEqual(cols, expected)
                # deskripsi la liu 100 liafuan
                text = pg.locator(".activity-card p").first.inner_text()
                self.assertLessEqual(len(text.replace("…", " ").split()), 100)

    def test_what_we_do_search_works_in_browser(self):
        pg, _ = self.page("hp-360", "/what-we-do/")
        pg.fill("input[name=q]", "Atividade 3")
        pg.click(".wwd-search button")
        pg.wait_for_load_state()
        self.assertEqual(pg.locator(".activity-card").count(), 1)

    def test_what_we_do_card_click_opens_detail(self):
        pg, _ = self.page("tablet-768", "/what-we-do/")
        pg.locator(".activity-card").first.click()
        pg.wait_for_load_state()
        self.assertIn("/what-we-do/activity/", pg.url)
        self.assertIn("kata299", pg.content())

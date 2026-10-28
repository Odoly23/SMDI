"""Unit test website publik: halaman, What We Do (ringkas/detail/cari), SEO."""
from django.test import TestCase, override_settings
from django.urls import reverse

from custom.models import Category
from .models import Activity, Article, ImpactStat, NewsPost, Program


def words(n, prefix="kata"):
    return " ".join(f"{prefix}{i}" for i in range(n))


class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="Doc PNDS", slug="doc-pnds", context="document")
        Program.objects.create(slug="pilar-1", title="Pilar 1", description="x", icon="bi-diagram-3", order=0)

    def test_main_pages_return_200(self):
        urls = [
            reverse("website:home"), reverse("website:who_we_are"),
            reverse("website:vision_mission"), reverse("website:what_we_do"),
            reverse("website:partners_networks"), reverse("website:current_donors"),
            reverse("website:news_list"), reverse("website:article_list"),
            reverse("website:contact"),
            reverse("website:program_detail", args=["pilar-1"]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_navbar_collapses_below_xl(self):
        """Menu desktop mak 9 item + login: hamburger to'o <1200px, la bele tabrakan ho logo."""
        html = self.client.get(reverse("website:home")).content.decode()
        self.assertIn("navbar-expand-xl", html)
        self.assertNotIn("navbar-expand-lg", html)

    def test_hero_carousel_has_accessible_controls(self):
        html = self.client.get(reverse("website:home")).content.decode()
        self.assertIn("carousel-control-prev", html)
        self.assertIn("carousel-control-next", html)


class WhatWeDoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.long = Activity.objects.create(tag="Riset", title="Aktivitas Panjang", description=words(300))
        cls.short = Activity.objects.create(tag="Advokasi", title="Aktivitas Pendek", description="Deskripsi singkat saja.")
        cls.hidden = Activity.objects.create(tag="Riset", title="Draft Rahasia", description="x", is_published=False)

    def get(self, **params):
        return self.client.get(reverse("website:what_we_do"), params)

    def test_description_is_truncated_to_100_words(self):
        r = self.get()
        self.assertContains(r, "kata99")
        self.assertNotContains(r, "kata100 ")
        self.assertNotContains(r, "kata299")

    def test_short_description_is_untouched(self):
        self.assertContains(self.get(), "Deskripsi singkat saja.")

    def test_unpublished_activity_hidden(self):
        r = self.get()
        self.assertNotContains(r, "Draft Rahasia")
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)

    def test_cards_link_to_detail(self):
        r = self.get()
        self.assertContains(r, self.long.get_absolute_url())
        self.assertContains(r, "View details")

    def test_search_by_title_description_and_tag(self):
        self.assertContains(self.get(q="Pendek"), "Aktivitas Pendek")
        self.assertNotContains(self.get(q="Pendek"), "Aktivitas Panjang")
        self.assertContains(self.get(q="singkat"), "Aktivitas Pendek")
        self.assertContains(self.get(q="Riset"), "Aktivitas Panjang")
        self.assertContains(self.get(q="tidak-ada-sama-sekali"), "No activities found.")

    def test_tag_filter(self):
        r = self.get(tag="Advokasi")
        self.assertContains(r, "Aktivitas Pendek")
        self.assertNotContains(r, "Aktivitas Panjang")

    def test_search_and_tag_combine(self):
        r = self.get(q="Panjang", tag="Advokasi")
        self.assertNotContains(r, "Aktivitas Panjang")
        self.assertNotContains(r, "Aktivitas Pendek")

    def test_tag_chips_list_only_published_tags(self):
        r = self.get()
        self.assertEqual(sorted(r.context["tags"]), ["Advokasi", "Riset"])

    def test_pagination_nine_per_page_and_keeps_query(self):
        for i in range(12):
            Activity.objects.create(tag="Massal", title=f"Massal {i:02d}", description="d")
        r = self.get(tag="Massal")
        self.assertEqual(len(r.context["page_obj"]), 9)
        self.assertTrue(r.context["page_obj"].has_next())
        self.assertContains(r, "tag=Massal&amp;page=2")
        r2 = self.get(tag="Massal", page=2)
        self.assertEqual(len(r2.context["page_obj"]), 3)

    def test_invalid_page_does_not_crash(self):
        self.assertEqual(self.get(page="abc").status_code, 200)
        self.assertEqual(self.get(page=9999).status_code, 200)

    def test_detail_shows_full_description(self):
        r = self.client.get(self.long.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "kata299")
        self.assertContains(r, "Aktivitas Panjang")
        self.assertContains(r, reverse("website:what_we_do"))

    def test_detail_unknown_pk_404(self):
        self.assertEqual(self.client.get(reverse("website:activity_detail", args=[99999])).status_code, 404)

    def test_program_area_tiles_are_links(self):
        p = Program.objects.create(slug="pilar-9", title="Pilar Sembilan", description="x", icon="bi-tree", order=9)
        self.assertContains(self.get(), p.get_absolute_url())

    def test_search_input_is_escaped(self):
        r = self.get(q='"><script>alert(1)</script>')
        self.assertNotContains(r, "<script>alert(1)</script>")


class SeoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.activity = Activity.objects.create(tag="Riset", title="Untuk Sitemap", description="d")
        NewsPost.objects.create(title="Berita Satu", slug="berita-satu", excerpt="e", body="b",
                                published_date="2026-01-01")

    def test_robots_txt(self):
        r = self.client.get("/robots.txt")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Disallow: /dashboard/")
        self.assertContains(r, "Sitemap: http://testserver/sitemap.xml")

    def test_sitemap_lists_content(self):
        r = self.client.get("/sitemap.xml")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, self.activity.get_absolute_url())
        self.assertContains(r, "/news/berita-satu/")
        self.assertNotContains(r, "/dashboard/")

    def test_canonical_link(self):
        r = self.client.get(reverse("website:what_we_do"))
        self.assertContains(r, '<link rel="canonical" href="http://testserver/what-we-do/">')

    @override_settings(GA_MEASUREMENT_ID="")
    def test_no_analytics_without_id(self):
        self.assertNotContains(self.client.get("/"), "googletagmanager")

    @override_settings(GA_MEASUREMENT_ID="G-TEST123456")
    def test_analytics_with_id(self):
        self.assertContains(self.client.get("/"), "G-TEST123456")


class ActivityDetailPageTests(TestCase):
    def setUp(self):
        self.items = [Activity.objects.create(tag="T", title=f"Aktividade {i}", description="kata " * 50, order=i)
                      for i in range(6)]

    def test_context_has_pager_and_limited_others(self):
        r = self.client.get(self.items[2].get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["prev_activity"].pk, self.items[1].pk)
        self.assertEqual(r.context["next_activity"].pk, self.items[3].pk)
        self.assertEqual(len(r.context["others"]), 4)
        self.assertNotIn(self.items[2].pk, [o.pk for o in r.context["others"]])
        self.assertGreaterEqual(r.context["read_minutes"], 1)

    def test_first_and_last_have_one_neighbour(self):
        self.assertIsNone(self.client.get(self.items[0].get_absolute_url()).context["prev_activity"])
        self.assertIsNone(self.client.get(self.items[-1].get_absolute_url()).context["next_activity"])

    def test_uses_compact_related_list_not_stretching_cards(self):
        html = self.client.get(self.items[0].get_absolute_url()).content.decode()
        self.assertIn("related-item", html)
        self.assertNotIn("mdi-card", html)
        self.assertIn("data-clamp", html)

    def test_navbar_has_grouped_dropdowns(self):
        html = self.client.get("/").content.decode()
        self.assertEqual(html.count("dropdown-toggle"), html.count('data-bs-toggle="dropdown"') - html.count('btn nav-auth-link dropdown-toggle'))
        for url in ("/who-we-are/", "/vision-mission/", "/partners-networks/", "/current-donors/", "/news/", "/articles/"):
            self.assertIn(f'class="dropdown-item" href="{url}"', html)


class HiddenDocumentsTests(TestCase):
    """Dokumen la publiku (default): menu la hatudu, URL 404, la iha iha sitemap."""
    def setUp(self):
        Category.objects.create(name="Doc PNDS", slug="doc-pnds", context="document")

    def test_documents_url_is_404_by_default(self):
        self.assertEqual(self.client.get("/documents/doc-pnds/").status_code, 404)

    def test_no_documents_menu_or_sitemap(self):
        html = self.client.get("/").content.decode()
        self.assertNotIn("/documents/", html)
        self.assertNotIn("/documents/", self.client.get("/sitemap.xml").content.decode())

    @override_settings(PUBLIC_DOCUMENTS=True)
    def test_can_be_turned_on_again(self):
        self.assertEqual(self.client.get("/documents/doc-pnds/").status_code, 200)
        self.assertIn("/documents/doc-pnds/", self.client.get("/").content.decode())


class SharingAndSeoTests(TestCase):
    def setUp(self):
        import datetime
        self.news = NewsPost.objects.create(title="Berita Tes", slug="berita-tes", excerpt="Ringkasan tes",
                                            body="isi", published_date=datetime.date(2026, 1, 1))
        self.act = Activity.objects.create(tag="T", title="Aktividade Tes", description="deskrisaun " * 30)

    def test_share_bar_and_open_graph_on_detail_pages(self):
        for url in (f"/news/{self.news.slug}/", self.act.get_absolute_url()):
            with self.subTest(url=url):
                html = self.client.get(url).content.decode()
                self.assertIn("data-share", html)
                self.assertIn("wa.me/?text=", html)
                self.assertIn("facebook.com/sharer", html)
                self.assertIn('property="og:type" content="article"', html)
                self.assertIn('property="og:url"', html)
                self.assertIn('property="og:image" content="http://testserver/', html)
                self.assertIn('name="twitter:title"', html)

    def test_og_title_matches_page(self):
        html = self.client.get(f"/news/{self.news.slug}/").content.decode()
        self.assertIn('property="og:title" content="Berita Tes"', html)
        self.assertIn('property="og:description" content="Ringkasan tes"', html)


class ImpactTests(TestCase):
    def test_auto_stats_from_database_when_no_manual_entries(self):
        from custom.models import Municipality
        dili = Municipality.objects.create(name="Dili")
        Activity.objects.create(tag="T", title="A1", description="x", municipality=dili)
        Activity.objects.create(tag="T", title="A2", description="x", municipality=dili)
        r = self.client.get("/")
        values = {s.get("key"): s["value"] for s in r.context["impact_stats"]}
        self.assertEqual(values["activities"], 2)
        self.assertEqual(values["municipalities"], 1)
        self.assertEqual(r.context["impact_points"], [{"name": "Dili", "count": 2, "lat": -8.5586, "lng": 125.5736}])
        self.assertContains(r, "impact-band")
        self.assertContains(r, 'id="impactPoints"')

    def test_manual_stats_override_auto(self):
        ImpactStat.objects.create(label="Suku", value=120, suffix="+", order=1)
        ImpactStat.objects.create(label="Hidden", value=9, is_active=False)
        r = self.client.get("/")
        self.assertEqual([s["label"] for s in r.context["impact_stats"]], ["Suku"])
        self.assertContains(r, "120")

    def test_no_empty_sections_without_data(self):
        r = self.client.get("/")
        self.assertNotContains(r, "impact-band")
        self.assertNotContains(r, "mdiImpactMap")

    def test_unknown_municipality_is_not_plotted(self):
        from custom.models import Municipality
        m = Municipality.objects.create(name="Tempat Asing")
        Activity.objects.create(tag="T", title="A", description="x", municipality=m)
        self.assertEqual(self.client.get("/").context["impact_points"], [])

    def test_municipality_filter_on_what_we_do(self):
        from custom.models import Municipality
        d = Municipality.objects.create(name="Dili"); e = Municipality.objects.create(name="Ermera")
        Activity.objects.create(tag="T", title="Di Dili", description="x", municipality=d)
        Activity.objects.create(tag="T", title="Di Ermera", description="x", municipality=e)
        r = self.client.get("/what-we-do/?mun=Dili")
        self.assertEqual([a.title for a in r.context["activities"]], ["Di Dili"])

    def test_geo_aliases(self):
        from .geo import centroid_for
        for name in ("Liquiçá", "liquica", "RAEOA", "Lautém", "Dili"):
            self.assertIsNotNone(centroid_for(name), name)
        self.assertIsNone(centroid_for("Mars"))


class SecurityHeaderTests(TestCase):
    def test_csp_on_public_pages_with_nonce(self):
        r = self.client.get("/")
        csp = r["Content-Security-Policy"]
        self.assertIn("default-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)
        self.assertIn("object-src 'none'", csp)
        self.assertNotIn("script-src 'self' 'unsafe-inline'", csp)
        self.assertIn("nonce-", csp)
        self.assertIn("camera=()", r["Permissions-Policy"])

    @override_settings(CSP_REPORT_ONLY=True)
    def test_report_only_switch(self):
        r = self.client.get("/")
        self.assertTrue(r.has_header("Content-Security-Policy-Report-Only"))
        self.assertFalse(r.has_header("Content-Security-Policy"))

    def test_dashboard_and_admin_exempt_from_csp(self):
        for path in ("/admin/login/", "/dashboard/login/"):
            self.assertFalse(self.client.get(path).has_header("Content-Security-Policy"), path)

    @override_settings(GA_MEASUREMENT_ID="G-TEST123")
    def test_inline_ga_script_has_matching_nonce(self):
        r = self.client.get("/")
        nonce = r["Content-Security-Policy"].split("'nonce-")[1].split("'")[0]
        self.assertIn(f'<script nonce="{nonce}">', r.content.decode())

    def test_no_inline_scripts_without_nonce_on_public_pages(self):
        import re
        for path in ("/", "/what-we-do/", "/who-we-are/", "/contact/"):
            html = self.client.get(path).content.decode()
            for tag in re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*type=\"application/json\")[^>]*>", html):
                self.assertIn("nonce=", tag, f"{path}: {tag}")

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_friendly_404_page(self):
        r = self.client.get("/halaman-tidak-ada/")
        self.assertEqual(r.status_code, 404)
        self.assertContains(r, "error-code", status_code=404)
        self.assertContains(r, 'href="/"', status_code=404)

    def test_500_page_renders_standalone(self):
        from django.template.loader import render_to_string
        html = render_to_string("500.html")
        self.assertIn("500", html)
        self.assertNotIn("{{", html)


class PerformanceTests(TestCase):
    def test_upload_is_downscaled_and_compressed(self):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        import random
        random.seed(1)
        im = Image.effect_noise((3200, 2400), 80).convert("RGB")
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=98)
        big = buf.getvalue()
        self.assertGreater(len(big), 800 * 1024)
        a = Activity.objects.create(tag="T", title="Foto besar", description="x",
                                    image=SimpleUploadedFile("foto.jpg", big, content_type="image/jpeg"))
        a.refresh_from_db()
        with Image.open(a.image.path) as saved:
            self.assertLessEqual(max(saved.size), 1600)
        self.assertLess(a.image.size, len(big) // 2)
        self.addCleanup(lambda: a.image.delete(save=False))

    def test_small_image_left_untouched(self):
        import io
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        buf = io.BytesIO(); Image.new("RGB", (300, 200), "red").save(buf, "PNG")
        data = buf.getvalue()
        a = Activity.objects.create(tag="T", title="Kecil", description="x",
                                    image=SimpleUploadedFile("kecil.png", data, content_type="image/png"))
        self.assertEqual(a.image.size, len(data))
        self.addCleanup(lambda: a.image.delete(save=False))

    def test_thumb_filter_creates_webp_and_falls_back(self):
        import io, os
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        from .images import thumb_url
        buf = io.BytesIO(); Image.new("RGB", (1200, 800), "blue").save(buf, "JPEG")
        a = Activity.objects.create(tag="T", title="Thumb", description="x",
                                    image=SimpleUploadedFile("t.jpg", buf.getvalue(), content_type="image/jpeg"))
        url = thumb_url(a.image, 400)
        self.assertTrue(url.endswith(".webp"), url)
        from django.conf import settings
        path = os.path.join(settings.MEDIA_ROOT, url.replace(settings.MEDIA_URL, "", 1))
        with Image.open(path) as t:
            self.assertEqual(t.width, 400)
        self.assertEqual(thumb_url(None, 400), "")
        self.addCleanup(lambda: (a.image.delete(save=False), os.path.exists(path) and os.remove(path)))

    def test_home_does_not_load_heavy_map_libraries_eagerly(self):
        html = self.client.get("/").content.decode()
        import re
        eager = re.findall(r'<script src="[^"]*leaflet[^"]*"', html)
        self.assertEqual(eager, [], "Leaflet/routing harus lazy")
        self.assertIn("maps-loader.js", html)
        self.assertIn("data-routing=", html)

    def test_assets_are_versioned_and_deferred(self):
        html = self.client.get("/").content.decode()
        self.assertRegex(html, r'theme\.css\?v=\w+')
        self.assertRegex(html, r'main\.js\?v=\w+" defer')
        self.assertIn('rel="preload"', html)
        self.assertIn('href="#main"', html)

    def test_gzip_enabled_for_html(self):
        r = self.client.get("/", HTTP_ACCEPT_ENCODING="gzip")
        self.assertEqual(r.get("Content-Encoding"), "gzip")

    def test_nav_programs_cached_and_invalidated(self):
        from django.core.cache import cache
        cache.clear()
        Program.objects.create(slug="p1", title="Pilar Satu", description="x", icon="bi-x", order=0)
        self.assertContains(self.client.get("/what-we-do/"), "Pilar Satu")
        Program.objects.create(slug="p2", title="Pilar Rua", description="x", icon="bi-x", order=1)
        self.assertContains(self.client.get("/what-we-do/"), "Pilar Rua")  # cache dibersihkan oleh signal

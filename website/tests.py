"""Unit test website publik: halaman, What We Do (ringkas/detail/cari), SEO."""
from django.test import TestCase, override_settings
from django.urls import reverse

from custom.models import Category
from .models import Activity, NewsPost, Program


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
            reverse("website:documents_by_category", args=["doc-pnds"]),
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

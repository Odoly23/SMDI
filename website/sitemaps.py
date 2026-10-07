from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, NewsPost, Program

STATIC_PAGES = [
    "website:home", "website:who_we_are", "website:vision_mission", "website:what_we_do",
    "website:partners_networks", "website:current_donors", "website:news_list",
    "website:article_list", "website:contact",
]
DOC_CATEGORIES = ["doc-pnds", "doc-oge", "doc-petroleum", "doc-statistika", "doc-outros"]


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return STATIC_PAGES

    def location(self, name):
        return reverse(name)


class DocumentCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return DOC_CATEGORIES

    def location(self, slug):
        return reverse("website:documents_by_category", kwargs={"cat_slug": slug})


class ProgramSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Program.objects.order_by("order")


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return NewsPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_date


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_date


SITEMAPS = {
    "pages": StaticSitemap,
    "documents": DocumentCategorySitemap,
    "programs": ProgramSitemap,
    "news": NewsSitemap,
    "articles": ArticleSitemap,
}

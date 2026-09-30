from django.urls import path
from . import views

app_name = "Website"

urlpatterns = [
    path("", views.home, name="home"),
    path("who-we-are/", views.who_we_are, name="who_we_are"),
    path("vision-mission/", views.vision_mission, name="vision_mission"),
    path("what-we-do/", views.what_we_do, name="what_we_do"),
    path("partners-networks/", views.partners_networks, name="partners_networks"),
    path("current-donors/", views.current_donors, name="current_donors"),
    path("program/<slug:slug>/", views.program_detail, name="program_detail"),
    path("documents/<slug:cat_slug>/", views.documents_by_category, name="documents_by_category"),
    path("news/", views.news_list, name="news_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/<slug:slug>/", views.article_detail, name="article_detail"),
    path("contact/", views.contact, name="contact"),
]

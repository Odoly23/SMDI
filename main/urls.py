from django.urls import path
from . import views, views_website

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Notísia (News)
    path("news/", views_website.news_list, name="news-list"),
    path("news/create/", views_website.news_create, name="news-create"),
    path("news/<int:pk>/edit/", views_website.news_update, name="news-update"),
    path("news/<int:pk>/delete/", views_website.news_delete, name="news-delete"),
    path("news/<int:pk>/gallery/", views_website.news_gallery, name="news-gallery"),
    path("news/image/<int:pk>/delete/", views_website.news_image_delete, name="news-image-delete"),

    # Artigu (Article)
    path("article/", views_website.article_list, name="article-list"),
    path("article/create/", views_website.article_create, name="article-create"),
    path("article/<int:pk>/edit/", views_website.article_update, name="article-update"),
    path("article/<int:pk>/delete/", views_website.article_delete, name="article-delete"),

    # Atividade (Activity)
    path("activity/", views_website.activity_list, name="activity-list"),
    path("activity/create/", views_website.activity_create, name="activity-create"),
    path("activity/<int:pk>/edit/", views_website.activity_update, name="activity-update"),
    path("activity/<int:pk>/delete/", views_website.activity_delete, name="activity-delete"),

    # Dokumentu (Document)
    path("document/", views_website.document_list, name="document-list"),
    path("document/create/", views_website.document_create, name="document-create"),
    path("document/<int:pk>/edit/", views_website.document_update, name="document-update"),
    path("document/<int:pk>/delete/", views_website.document_delete, name="document-delete"),
]

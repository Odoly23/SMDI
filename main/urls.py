from django.urls import path
from . import views, views_website, views_org, views_inbox, views_singleton, views_lookup

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

    # Programa (Pilar / Sub-Outcome)
    path("program/", views_org.program_list, name="program-list"),
    path("program/create/", views_org.program_create, name="program-create"),
    path("program/<int:pk>/edit/", views_org.program_update, name="program-update"),
    path("program/<int:pk>/delete/", views_org.program_delete, name="program-delete"),

    # Organigrama (OrgMember)
    path("orgmember/", views_org.orgmember_list, name="orgmember-list"),
    path("orgmember/create/", views_org.orgmember_create, name="orgmember-create"),
    path("orgmember/<int:pk>/edit/", views_org.orgmember_update, name="orgmember-update"),
    path("orgmember/<int:pk>/delete/", views_org.orgmember_delete, name="orgmember-delete"),

    # Fundador (Founder)
    path("founder/", views_org.founder_list, name="founder-list"),
    path("founder/create/", views_org.founder_create, name="founder-create"),
    path("founder/<int:pk>/edit/", views_org.founder_update, name="founder-update"),
    path("founder/<int:pk>/delete/", views_org.founder_delete, name="founder-delete"),

    # Parseiru / Doador (Partner)
    path("partner/", views_inbox.partner_list, name="partner-list"),
    path("partner/create/", views_inbox.partner_create, name="partner-create"),
    path("partner/<int:pk>/edit/", views_inbox.partner_update, name="partner-update"),
    path("partner/<int:pk>/delete/", views_inbox.partner_delete, name="partner-delete"),

    # Mensajen Kontaktu (ContactMessage inbox)
    path("message/", views_inbox.message_list, name="message-list"),
    path("message/<int:pk>/", views_inbox.message_detail, name="message-detail"),
    path("message/<int:pk>/delete/", views_inbox.message_delete, name="message-delete"),

    # Slide Hero
    path("slide/", views_singleton.slide_list, name="slide-list"),
    path("slide/create/", views_singleton.slide_create, name="slide-create"),
    path("slide/<int:pk>/edit/", views_singleton.slide_update, name="slide-update"),
    path("slide/<int:pk>/delete/", views_singleton.slide_delete, name="slide-delete"),

    # Konteudu singleton
    path("vision-mission/", views_singleton.vision_mission_edit, name="vision-mission-edit"),
    path("who-we-are/", views_singleton.who_we_are_edit, name="who-we-are-edit"),
    path("site-config/", views_singleton.site_config_edit, name="site-config-edit"),

    # Kategoria (Category)
    path("category/", views_lookup.category_list, name="category-list"),
    path("category/create/", views_lookup.category_create, name="category-create"),
    path("category/<int:pk>/edit/", views_lookup.category_update, name="category-update"),
    path("category/<int:pk>/delete/", views_lookup.category_delete, name="category-delete"),

    # Munisípiu (Municipality)
    path("municipality/", views_lookup.municipality_list, name="municipality-list"),
    path("municipality/create/", views_lookup.municipality_create, name="municipality-create"),
    path("municipality/<int:pk>/edit/", views_lookup.municipality_update, name="municipality-update"),
    path("municipality/<int:pk>/delete/", views_lookup.municipality_delete, name="municipality-delete"),

    # Postu Administrativu (AdministrativePost)
    path("adminpost/", views_lookup.adminpost_list, name="adminpost-list"),
    path("adminpost/create/", views_lookup.adminpost_create, name="adminpost-create"),
    path("adminpost/<int:pk>/edit/", views_lookup.adminpost_update, name="adminpost-update"),
    path("adminpost/<int:pk>/delete/", views_lookup.adminpost_delete, name="adminpost-delete"),

    # Tinan (Year)
    path("year/", views_lookup.year_list, name="year-list"),
    path("year/create/", views_lookup.year_create, name="year-create"),
    path("year/<int:pk>/edit/", views_lookup.year_update, name="year-update"),
    path("year/<int:pk>/delete/", views_lookup.year_delete, name="year-delete"),
]

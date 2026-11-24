from django.contrib import admin
from django.urls import path

from recipes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("index.html", views.home, name="home_page"),
    path("recipes.html", views.recipes, name="recipes"),
    path("about.html", views.about, name="about"),
    path("contact.html", views.contact, name="contact"),
    path("login.html", views.login_view, name="login"),
    path("register.html", views.register_view, name="register"),
    path("guest/", views.guest_view, name="guest"),
    path("logout/", views.logout_view, name="logout"),
]

from django.urls import path

from listings.views import index, register, home

urlpatterns = [
    path("", index, name="index"),
    path("register", register, name="register"),
    path("home", home, name="home"),
]

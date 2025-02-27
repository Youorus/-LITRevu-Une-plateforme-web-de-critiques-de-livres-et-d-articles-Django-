from django.contrib.auth.views import LogoutView
from django.urls import path

from listings.views import index, register, flux

urlpatterns = [
    path("", index, name="index"),
    path("register", register, name="register"),
    path("flux", flux, name="flux"),
    path("logout", LogoutView.as_view(), name="logout"),
]

from django.urls import path
from listings.views import index, register, flux, logout_view, new_ticket

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("flux/", flux, name="flux"),
    path("logout/", logout_view, name="logout"),  # Utilisation de la fonction logout_view
    path("tickets/new/", new_ticket, name="new_ticket"),
]

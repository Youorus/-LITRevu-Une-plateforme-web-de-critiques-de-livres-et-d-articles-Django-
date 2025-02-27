from django.urls import path
from listings.views import index, register, flux, logout_view, new_ticket, new_review, create_ticket_and_review

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("flux/", flux, name="flux"),
    path("logout/", logout_view, name="logout"),  # Utilisation de la fonction logout_view
    path("tickets/new/", new_ticket, name="new_ticket"),
    path("review/new/", new_review, name="new_review"),
    path("ticket_and_review/new/", create_ticket_and_review, name="new_ticket_and_review"),
]

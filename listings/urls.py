from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from listings.views import index, register, flux, logout_view, new_ticket, new_review, create_ticket_and_review, posts, \
    edit_ticket, edit_review, follow_view, delete_ticket, delete_review

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("flux/", flux, name="flux"),
    path("logout/", logout_view, name="logout"),  # Utilisation de la fonction logout_view
    path("tickets/new/", new_ticket, name="new_ticket"),
    path("review/new/", new_review, name="new_review"),
    path("ticket_and_review/new/", create_ticket_and_review, name="new_ticket_and_review"),
    path('posts/', posts, name="posts"),
    path("ticket/edit/<int:ticket_id>/", edit_ticket, name="edit_ticket"),
    path("review/edit/<int:review_id>/", edit_review, name="edit_review"),
    path("follow/", follow_view, name="follow_view"),
    path('flux/', flux, name='flux'),
    path('review/new/<int:ticket_id>/', new_review, name='new_review_ticket'),
    path("ticket/delete/<int:ticket_id>/", delete_ticket, name="delete_ticket"),
    path("review/delete/<int:review_id>/", delete_review, name="delete_review"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
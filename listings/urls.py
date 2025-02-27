from django.urls import path

from listings.views import index

urlpatterns = [
    path("", index, name="index"),
]

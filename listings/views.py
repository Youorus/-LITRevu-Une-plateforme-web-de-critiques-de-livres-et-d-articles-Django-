from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from listings.forms import UserRegistrationForm


# Create your views here.
def index(request):
    return render(request, "index.html")


def register(request):
    """Gère l'inscription des utilisateurs avec affichage des erreurs"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect("home")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegistrationForm()

    return render(request, "register_form.html", {"form": form})

def home(request):
    return render(request, "home.html")
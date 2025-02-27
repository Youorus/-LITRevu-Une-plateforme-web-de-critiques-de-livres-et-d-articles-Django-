from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from listings.forms import UserRegistrationForm


# Create your views here.
def index(request):
    """Page d'accueil qui affiche le formulaire de connexion si l'utilisateur n'est pas connecté"""
    if request.user.is_authenticated:
        return redirect("flux")  # Redirige vers /home si l'utilisateur est connecté

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("flux")  # Redirige vers /home après connexion
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "index.html")


def register(request):
    """Gère l'inscription des utilisateurs avec affichage des erreurs"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect("flux")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserRegistrationForm()

    return render(request, "register_form.html", {"form": form})

def logout(request):
    """Gère la déconnexion des utilisateurs"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("index")

@login_required(login_url="/")
def flux(request):
    return render(request, "flux.html")
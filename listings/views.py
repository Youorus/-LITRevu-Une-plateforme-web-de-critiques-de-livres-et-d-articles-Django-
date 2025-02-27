from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from listings.forms import UserRegistrationForm, TicketForm, ReviewForm
from listings.models import Ticket


def index(request):
    """Page d'accueil qui affiche le formulaire de connexion si l'utilisateur n'est pas connecté"""
    if request.user.is_authenticated:
        print("Utilisateur connecté, redirection vers /flux/")  # Ajoute ce log
        return redirect("flux")  # Redirige vers /flux si connecté

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"Connexion réussie : {user.username}, redirection vers /flux/")  # Debugging
            return redirect("flux")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, "index.html")



def register(request):
    """Gère l'inscription des utilisateurs avec affichage des erreurs"""
    if request.user.is_authenticated:
        return redirect("flux")  # Empêche un utilisateur connecté d'accéder à l'inscription

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


def logout_view(request):
    """Gère la déconnexion des utilisateurs"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("index")


@login_required(login_url="/")
def flux(request):
    """Page principale après connexion"""
    messages.success(request, f"Bienvenue, {request.user.username} ! 🎉")
    return render(request, "flux.html")


@login_required(login_url="/")
def new_ticket(request):
    """Vue pour créer un nouveau ticket"""
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Associer le ticket à l'utilisateur connecté
            ticket.save()
            messages.success(request, "Votre demande de critique a été publiée !")
            return redirect("flux")  # Redirige vers la page principale après soumission
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = TicketForm()

    return render(request, "new_ticket.html", {"form": form})


@login_required(login_url="/")
def new_review(request):
    """Vue pour créer une critique d'un ticket existant"""


    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Votre critique a été ajoutée avec succès !")
            return redirect("flux")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ReviewForm()

    return render(request, "new_review.html", {"form": form})

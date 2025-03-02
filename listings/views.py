from itertools import chain
from django.db.models import Value, CharField, Q, Exists, OuterRef
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from listings import models
from listings.forms import UserRegistrationForm, TicketForm, ReviewForm
from listings.models import Ticket, Review, User, UserFollows


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
            return redirect("flux")
    else:
        form = TicketForm()

    return render(request, "new_ticket.html", {
        "form": form
    })


@login_required(login_url="/")
def new_review(request, ticket_id=None):
    """
    Vue pour créer une critique d'un ticket existant ou sans ticket.

    - Si `ticket_id` est fourni, la critique est associée à un ticket spécifique.
    - Sinon, l'utilisateur peut écrire une critique librement.
    """

    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associe la critique à l'utilisateur connecté
            if ticket:
                review.ticket = ticket  # Associe la critique au ticket si fourni
            review.save()

            messages.success(request, "Votre critique a été ajoutée avec succès !")

            # 🔹 Redirige vers la section du ticket après soumission
            return redirect("flux")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ReviewForm()

    return render(request, "new_review.html", {
        "form": form,
        "ticket": ticket
    })

@login_required
def create_ticket_and_review(request):
    """Vue pour créer un ticket et une critique en même temps"""

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            print("✅ Formulaires valides ! Enregistrement en base...")
        if ticket_form.is_valid() and review_form.is_valid():
            # Enregistrer le ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Enregistrer la critique associée au ticket
            review = review_form.save(commit=False)
            review.ticket = ticket  # Associer la critique au ticket créé
            review.user = request.user
            review.save()

            messages.success(request, "Votre ticket et votre critique ont été publiés avec succès !")
            return redirect("flux")  # ✅ Redirige vers le flux après soumission

        else:
            messages.error(request, "Veuillez corriger les erreurs des formulaires.")

    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, "new_ticket_and_review.html", {
        "ticket_form": ticket_form,
        "review_form": review_form,
        "edit_mode": True,
    })


def posts(request):
    """Récupère les tickets de l'utilisateur actuel et les envoie à la vue"""
    user_tickets = Ticket.objects.filter(user=request.user).order_by("-created_at")  # Tri par date décroissante
    """Récupère et affiche les critiques de l'utilisateur connecté"""
    reviews = Review.objects.filter(user=request.user).order_by("-time_created")  # Trier par date descendante

    return render(request, "posts.html", {"user_tickets": user_tickets, "reviews": reviews})

@login_required(login_url="/")
def edit_ticket(request, ticket_id):
    """Vue pour modifier un ticket existant"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre ticket a été mis à jour avec succès !")
            return redirect("posts")  # Redirige vers la liste des posts après modification
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = TicketForm(instance=ticket)

    return render(request, "edit_ticket.html", {
        "form": form,
        "edit_mode": True,  # Mode édition
        "ticket": ticket  # On passe le ticket existant
    })

@login_required(login_url="/")
def edit_review(request, review_id):
    """Vue pour modifier une critique existante sans modifier le ticket"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket  # Récupération du ticket lié à la critique
    print(review.rating)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a été mise à jour avec succès !")
            return redirect("posts")  # Redirige vers les posts de l'utilisateur
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = ReviewForm(instance=review)

    return render(request, "edit_review.html", {
        "form": form,
        "ticket": ticket,  # On envoie le ticket à la template pour l'afficher
        "review": review,
        "edit_mode": True,  # Indicateur pour l'affichage dynamique
    })

@login_required
def follow_view(request):
    """Affiche les abonnés, abonnements et permet de rechercher des utilisateurs"""
    query = request.GET.get('search', '')

    # Récupère les abonnements et abonnés de l'utilisateur connecté
    following = UserFollows.objects.filter(user=request.user).select_related("followed_user")
    followers = UserFollows.objects.filter(followed_user=request.user).select_related("user")

    # Recherche d'un utilisateur
    search_results = User.objects.exclude(id=request.user.id).filter(username__icontains=query) if query else []

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        target_user = get_object_or_404(User, id=user_id)

        if action == "follow":
            UserFollows.objects.get_or_create(user=request.user, followed_user=target_user)
            messages.success(request, f"Vous suivez maintenant {target_user.username}.")
        elif action == "unfollow":
            UserFollows.objects.filter(user=request.user, followed_user=target_user).delete()
            messages.success(request, f"Vous ne suivez plus {target_user.username}.")

        return redirect("follow_view")

    return render(request, "follow.html", {
        "following": following,
        "followers": followers,
        "search_results": search_results,
        "query": query
    })



@login_required
def flux(request):
    """
    Affiche le flux d'activité de l'utilisateur connecté avec :
    - Les billets et avis des utilisateurs suivis
    - Les billets et avis de l'utilisateur connecté
    - Les avis en réponse aux billets de l'utilisateur connecté
    """
    user = request.user

    # 🔹 Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=user).values_list("followed_user", flat=True)

    # 🔹 Récupérer toutes les critiques visibles par l'utilisateur
    reviews = Review.objects.filter(
        Q(user__in=followed_users) |  # Critiques des utilisateurs suivis
        Q(user=user) |  # Critiques de l'utilisateur connecté
        Q(ticket__user=user)  # Critiques en réponse aux billets de l'utilisateur connecté
    ).annotate(content_type=Value('REVIEW', output_field=CharField()))

    # ✅ Récupérer uniquement les tickets **qui n'ont pas encore de critiques affichées**
    tickets_with_reviews = reviews.values_list("ticket_id", flat=True)

    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) |  # Billets des utilisateurs suivis
        Q(user=user)  # Billets de l'utilisateur connecté
    ).exclude(id__in=tickets_with_reviews)  # ✅ Exclure les tickets qui ont déjà une critique

    tickets = tickets.annotate(content_type=Value('TICKET', output_field=CharField()))

    # 🔹 Fusionner billets et critiques, triés du plus récent au plus ancien
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: getattr(post, 'time_created', getattr(post, 'created_at', None)),
        reverse=True
    )

    return render(request, "flux.html", {"posts": posts})


@login_required
def delete_ticket(request, ticket_id):
    """Supprime un ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.delete()
    messages.success(request, "Votre ticket a été supprimé avec succès !")
    return redirect("posts")


@login_required
def delete_review(request, review_id):
    """Supprime une critique"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    messages.success(request, "Votre critique a été supprimée avec succès !")
    return redirect("posts")



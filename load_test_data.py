import os
import random

import django

# ✅ Configuration Django AVANT les imports de modèles
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "LITRevuProject.settings"
)  # Remplace par le bon nom
django.setup()

from django.contrib.auth import get_user_model

from listings.models import (  # Remplace "listings" par ton application réelle
    Review,
    Ticket,
)

# ✅ Données réalistes pour les tests
USERNAMES = ["alice", "bob", "charlie", "diana", "emma", "frank", "george", "hannah"]
PASSWORD = "Test1234"

TICKET_TITLES = [
    "Erreur critique sur le site",
    "Amélioration de l'interface utilisateur",
    "Problème d'affichage mobile",
    "Demande de nouvelle fonctionnalité",
    "Bug lors de l'inscription",
    "Optimisation des performances",
    "Sécurité des données à revoir",
    "Refonte du design du tableau de bord",
]

TICKET_DESCRIPTIONS = [
    "Le site plante après l'envoi du formulaire de contact.",
    "L'UX pourrait être améliorée en ajoutant des animations plus fluides.",
    "Sur mobile, les boutons sont trop petits et difficiles à cliquer.",
    "Une fonctionnalité permettant de filtrer les tickets serait très utile.",
    "L'inscription ne fonctionne pas avec certaines adresses email.",
    "Le chargement de la page d'accueil est trop lent, optimisation nécessaire.",
    "Le stockage des mots de passe ne semble pas sécurisé, vérifier le chiffrement.",
    "Un redesign du tableau de bord rendrait l'interface plus agréable.",
]

REVIEW_HEADLINES = [
    "Expérience incroyable",
    "Peut mieux faire",
    "Super service client",
    "Trop de bugs",
    "Interface fluide et agréable",
    "Difficile à utiliser",
    "Excellente amélioration",
    "Manque quelques fonctionnalités",
]

REVIEW_BODIES = [
    "J'ai adoré utiliser cette application, très intuitive !",
    "Quelques bugs mineurs mais globalement une bonne expérience.",
    "Service client réactif et à l'écoute, c'est appréciable.",
    "Trop de crashs et de bugs, cela nuit à l'expérience utilisateur.",
    "L'application est bien pensée et agréable à utiliser.",
    "Difficile à comprendre pour un nouvel utilisateur, manque de tutoriels.",
    "Les mises à jour récentes ont apporté beaucoup d'améliorations.",
    "Certaines fonctionnalités sont absentes mais ça reste correct.",
]


def load_test_data():
    """Ajoute des données de test SANS supprimer les anciennes."""
    print("🚀 Chargement des données de test...")

    User = get_user_model()
    users = []

    # ✅ Ajouter des utilisateurs de test UNIQUEMENT s'ils n'existent pas déjà
    for username in USERNAMES:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(PASSWORD)
            user.save()
            print(f"👤 Utilisateur créé : {username}")
        users.append(user)

    # ✅ Ajouter des tickets de test (évite les doublons)
    for _ in range(20):
        user = random.choice(users)
        title = random.choice(TICKET_TITLES)
        description = random.choice(TICKET_DESCRIPTIONS)

        # Vérifie si un ticket avec ce titre existe déjà
        if not Ticket.objects.filter(title=title, user=user).exists():
            ticket = Ticket.objects.create(
                title=title, description=description, user=user
            )
            print(f"🎫 Ticket ajouté : {title} (par {user.username})")

    # ✅ Ajouter des critiques de test (avec un Ticket obligatoire)
    for _ in range(20):
        user = random.choice(users)
        headline = random.choice(REVIEW_HEADLINES)
        body = random.choice(REVIEW_BODIES)
        rating = random.randint(1, 5)

        # 🟢 Sélectionner un ticket aléatoire existant (OBLIGATOIRE)
        ticket = Ticket.objects.order_by("?").first()  # Récupère un ticket au hasard

        if ticket:  # Vérifie qu'un ticket existe avant de créer la review
            review = Review.objects.create(
                headline=headline,
                body=body,
                rating=rating,
                user=user,
                ticket=ticket,  # 🔴 Ajoute un Ticket obligatoire ici
            )
            print(
                f"⭐ Critique ajoutée : {headline} (Note: {rating}/5 par {user.username}, pour le ticket '{ticket.title}')"
            )
        else:
            print("❌ Aucune critique ajoutée car aucun ticket disponible.")


if __name__ == "__main__":
    load_test_data()

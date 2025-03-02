import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Ticket, Review, UserFollows

User = get_user_model()


class Command(BaseCommand):
    help = "Supprime les données existantes et charge des données de test"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("🚨 Suppression des anciennes données..."))

        # Supprimer les données existantes
        UserFollows.objects.all().delete()
        Review.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("✅ Données supprimées."))

        # 🔹 Création d'utilisateurs de test
        self.stdout.write(self.style.WARNING("👤 Création des utilisateurs..."))
        users = []
        usernames = ["alice", "bob", "charlie", "david", "eve"]
        for username in usernames:
            user = User.objects.create_user(username=username, password="Test1234!")
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f" - Utilisateur {username} créé."))

        # 🔹 Création de tickets de test
        self.stdout.write(self.style.WARNING("📌 Création de tickets..."))
        tickets = []
        for i in range(5):
            user = random.choice(users)
            ticket = Ticket.objects.create(
                user=user,
                title=f"Ticket {i + 1}",
                description=f"Description du ticket {i + 1}.",
            )
            tickets.append(ticket)
            self.stdout.write(self.style.SUCCESS(f" - Ticket {ticket.title} créé par {user.username}."))

        # 🔹 Création de critiques
        self.stdout.write(self.style.WARNING("✍️ Création de critiques..."))
        for i in range(5):
            ticket = random.choice(tickets)
            user = random.choice([u for u in users if u != ticket.user])  # Exclure l'auteur du ticket
            review = Review.objects.create(
                user=user,
                ticket=ticket,
                rating=random.randint(0, 5),
                headline=f"Critique {i + 1}",
                body=f"Texte de la critique {i + 1}.",
            )
            self.stdout.write(self.style.SUCCESS(f" - Critique '{review.headline}' ajoutée à {ticket.title}."))

        # 🔹 Création des abonnements entre utilisateurs
        self.stdout.write(self.style.WARNING("🔗 Création des relations de suivi..."))
        for user in users:
            followed_users = random.sample([u for u in users if u != user], k=2)  # Suivre 2 autres utilisateurs
            for followed in followed_users:
                UserFollows.objects.create(user=user, followed_user=followed)
                self.stdout.write(self.style.SUCCESS(f" - {user.username} suit {followed.username}."))

        self.stdout.write(self.style.SUCCESS("🎉 Données de test chargées avec succès !"))

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour gérer uniquement les utilisateurs normaux"""

    def create_user(self, username, password=None):
        """Créer un utilisateur normal"""
        user = self.model(username=username)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Modèle utilisateur sans email"""

    username = models.CharField(
        max_length=150, unique=True  # Vérification dans la base de données
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"  # Plus besoin d'email ici
    REQUIRED_FIELDS = []  # Supprime l'email des champs obligatoires

    def __str__(self):
        return self.username


from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """Modèle pour une demande de critique"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets"
    )
    title = models.CharField(
        max_length=128, error_messages={"blank": "Le titre est obligatoire."}
    )
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (par {self.user.username})"


class Review(models.Model):
    """Modèle pour une critique (review) d'un livre ou d'un article."""

    ticket = models.ForeignKey(
        "Ticket", on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    headline = models.CharField(
        max_length=128, error_messages={"blank": "Le titre est obligatoire."}
    )
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Critique de {self.user.username} sur {self.ticket.title} - {self.rating}⭐"


class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"

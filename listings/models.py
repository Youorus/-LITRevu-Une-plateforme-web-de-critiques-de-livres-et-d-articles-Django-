from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour gérer uniquement les utilisateurs normaux"""

    def create_user(self, username, email, password=None):
        """Créer un utilisateur normal"""
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire")
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """Modèle utilisateur simplifié (sans super admin)"""

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(3, message="Le nom d'utilisateur doit contenir au moins 3 caractères."),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores (_)."
            )
        ]
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Veuillez entrer une adresse email valide.")]
    )
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8, message="Le mot de passe doit contenir au moins 8 caractères.")]
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    # Obligatoire pour Django mais inutilisé
    is_active = models.BooleanField(default=True)  # L'utilisateur peut être désactivé

    objects = CustomUserManager()

    # Configuration pour l'authentification Django
    USERNAME_FIELD = "username"  # Champ utilisé pour l'authentification
    REQUIRED_FIELDS = ["email"]  # Champs obligatoires lors de create_user

    def __str__(self):
        return self.username

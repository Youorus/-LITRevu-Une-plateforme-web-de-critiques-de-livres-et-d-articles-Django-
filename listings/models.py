from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
        max_length=150,
        unique=True  # Vérification dans la base de données
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

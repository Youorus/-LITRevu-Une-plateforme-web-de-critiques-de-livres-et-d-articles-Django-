from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)  # Nom d'utilisateur unique
    password = models.CharField(max_length=128)  # Stockage du mot de passe (hashé côté vue)
    date_joined = models.DateTimeField(auto_now_add=True)  # Date d'inscription automatique

    def __str__(self):
        return self.username

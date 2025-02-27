from django import forms
from django.core.exceptions import ValidationError
from .models import User
import re


class UserRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription sans email avec validation avancée"""

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"}),
    )

    class Meta:
        model = User
        fields = ["username"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
        }

    def clean_username(self):
        """Vérifie que le nom d'utilisateur est unique et a une longueur correcte"""
        username = self.cleaned_data.get("username")

        # Vérifier si le nom d'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")

        # Vérifier la longueur du nom d'utilisateur
        if len(username) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")
        if len(username) > 10:
            raise ValidationError("Le nom d'utilisateur ne peut pas dépasser 30 caractères.")

        return username

    def clean_password1(self):
        """Valide le mot de passe : 8 caractères, 1 majuscule, 1 chiffre"""
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
        if not re.search(r'[0-9]', password1):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        return password1

    def clean_password2(self):
        """Vérifie que les mots de passe correspondent"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        """Créer un utilisateur avec un mot de passe haché"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

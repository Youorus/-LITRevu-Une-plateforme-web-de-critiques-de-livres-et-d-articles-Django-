from django import forms
from django.core.exceptions import ValidationError
from .models import User, Ticket, Review
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


class TicketForm(forms.ModelForm):
    """Formulaire de création d'un ticket avec validation"""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer des classes Tailwind aux champs
        self.fields["title"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "maxlength": "128"  # Ajout de la restriction HTML
        })
        self.fields["description"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "maxlength": "2048" ,
            "rows": "4"# Ajout de la restriction HTML
        })
        self.fields["image"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        })

    def clean_title(self):
        """Validation du titre : doit contenir entre 3 et 128 caractères et être unique"""
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        if len(title) > 128:
            raise forms.ValidationError("Le titre ne peut pas dépasser 128 caractères.")
        if Ticket.objects.filter(title=title).exists():
            raise forms.ValidationError("Un ticket avec ce titre existe déjà.")
        return title

    def clean_description(self):
        """Validation de la description : facultative mais limitée à 2048 caractères"""
        description = self.cleaned_data.get("description", "").strip()
        if description and len(description) > 2048:
            raise forms.ValidationError("La description ne peut pas dépasser 2048 caractères.")
        return description

class ReviewForm(forms.ModelForm):
    """Formulaire pour créer une critique avec validation"""

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Appliquer des classes Tailwind aux champs
        self.fields["headline"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Titre de la critique"
        })
        self.fields["body"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "placeholder": "Écrivez votre critique (optionnel)",
            "rows": "4"
        })
        self.fields["rating"].widget.attrs.update({
            "class": "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
            "type": "number",
            "min": "0",
            "max": "5",
            "step": "1"
        })

    def clean_headline(self):
        """Validation du titre"""
        headline = self.cleaned_data.get("headline", "").strip()
        if len(headline) < 3:
            raise forms.ValidationError("Le titre doit contenir au moins 3 caractères.")
        return headline

    def clean_rating(self):
        """Validation de la note (rating)"""
        rating = self.cleaned_data.get("rating")
        if rating is None or not (0 <= rating <= 5):
            raise forms.ValidationError("La note doit être comprise entre 0 et 5.")
        return rating
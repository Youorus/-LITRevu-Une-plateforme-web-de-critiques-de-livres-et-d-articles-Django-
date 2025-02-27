# Generated by Django 4.2.19 on 2025-02-27 13:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(3, message="Le nom d'utilisateur doit contenir au moins 3 caractères."), django.core.validators.RegexValidator(message="Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores (_).", regex='^[a-zA-Z0-9_]+$')])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='Veuillez entrer une adresse email valide.')])),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8, message='Le mot de passe doit contenir au moins 8 caractères.')])),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

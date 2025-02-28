# 📚 LITReview - Plateforme de Critiques & Abonnements

LITReview est une application web permettant aux utilisateurs de **publier des demandes de critiques**, **écrire des critiques** et **s'abonner à d'autres utilisateurs** pour suivre leurs publications.

---

## 🚀 **Fonctionnalités Principales**
- 📌 **Création de Tickets** : Demande de critiques sur un sujet ou un livre.
- ⭐ **Ajout de Critiques** : Répondre aux tickets en postant une critique avec une note (0 à 5 étoiles).
- 👥 **Système d'Abonnements** : Suivre et se désabonner d'autres utilisateurs.
- 🔍 **Recherche d'Utilisateurs** : Trouver d'autres utilisateurs et voir leurs publications.
- 🏠 **Flux Personnalisé** : Voir les publications des utilisateurs suivis.
- 🔐 **Authentification** : Inscription et connexion sécurisées.

---

## 🛠 **Technologies Utilisées**
- **Backend** : Django 4.x (Python)
- **Base de données** : SQLite (peut être remplacé par PostgreSQL/MySQL)
- **Frontend** : HTML, CSS (TailwindCSS)
- **Gestion des utilisateurs** : Django Authentication

---

## 👥 **Installation et Configuration**
### **1️⃣ Cloner le projet**
```sh
git clone https://github.com/ton_nom_utilisateur/LITReview.git
cd LITReview
```

### **2️⃣ Créer un environnement virtuel et l'activer**
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

### **3️⃣ Installer les dépendances**
```sh
pip install -r requirements.txt
```

### **4️⃣ Appliquer les migrations**
```sh
python manage.py migrate
```


### **6️⃣ Lancer le serveur local**
```sh
python manage.py runserver
```
Accède au site via : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📉 **Modèles de la Base de Données**
### **1️⃣ UserFollows (Gestion des abonnements)**
- **user** (_ForeignKey_) : L'utilisateur qui suit quelqu'un.
- **followed_user** (_ForeignKey_) : L'utilisateur suivi.
- **unique_together** : Un utilisateur ne peut suivre une autre personne qu'une seule fois.

### **2️⃣ Ticket (Demandes de critiques)**
- **user** (_ForeignKey_) : L'auteur du ticket.
- **title** (_CharField_) : Titre de la demande.
- **description** (_TextField_) : Détails sur la demande.
- **image** (_ImageField_) : Image optionnelle.
- **created_at** (_DateTimeField_) : Date de création.

### **3️⃣ Review (Critiques)**
- **ticket** (_ForeignKey_) : Ticket concerné par la critique.
- **user** (_ForeignKey_) : Auteur de la critique.
- **rating** (_PositiveSmallIntegerField_) : Note entre 0 et 5.
- **headline** (_CharField_) : Titre de la critique.
- **body** (_TextField_) : Texte de la critique.
- **time_created** (_DateTimeField_) : Date de création.

---

## 🌈 **Interface Utilisateur**
### **📍 Pages principales**
- 🏠 **Accueil** : Connexion / Inscription
- 📃 **Flux** : Voir les tickets et critiques des abonnements.
- ✍️ **Publier un Ticket & une Critique**
- 📚 **Mes Publications** : Voir ses propres publications.
- 👤 **Abonnements** : Gérer les utilisateurs suivis et rechercher de nouveaux utilisateurs.

---


## 📧 **Contact**
👤 **Auteur** : Marc  
📩 **Email** : [mtakoumba@gmail.com](mailto:mtakoumba@gmail.com)  
 **Supervision** : [Openclassrooms](https://litreview.com)  

---

### ⭐ **Si ce projet vous plaît, laissez un ⭐ sur GitHub !**


# 🌸 ESMT Tasks — Application de Gestion des Tâches Collaboratives

## 📋 Description

ESMT Tasks est une application web de gestion des tâches collaboratives développée avec **Django** (backend) et **React** (frontend). Elle permet aux étudiants et professeurs de l'ESMT de collaborer sur des projets, gérer des tâches, et suivre les performances avec un système de primes.

---

## 🛠️ Stack Technique

| Technologie           | Version  | Rôle                         |
|-----------------------|----------|------------------------------|
| Python                | 3.12.9   | Langage backend              |
| Django                | 6.0.3    | Framework backend            |
| Django REST Framework | latest   | API REST                     |
| Django Channels       | latest   | WebSockets (chat temps réel) |
| Daphne                | latest   | Serveur ASGI                 |
| React                 | 18       | Framework frontend           |
| Vite                  | latest   | Build tool React             |
| Chart.js              | latest   | Graphiques                   |
| @hello-pangea/dnd     | latest   | Drag & Drop Kanban           |

---

## 📁 Structure du Projet

```
esmt_tasks/                  ← Backend Django
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── api_urls.py
│   └── asgi.py
├── accounts/                ← Gestion utilisateurs
├── projects/                ← Gestion projets
├── tasks/                   ← Gestion tâches
├── chat/                    ← Chat temps réel
├── templates/               ← Templates HTML Django
└── manage.py

esmt_frontend/               ← Frontend React
├── src/
│   ├── api/axios.js
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Chat.jsx
│   │   ├── Charts.jsx
│   │   ├── Notifications.jsx
│   │   ├── Recherche.jsx
│   │   └── ThemeToggle.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Projets.jsx
│   │   ├── ProjetDetail.jsx
│   │   ├── ProjetMembres.jsx
│   │   ├── Kanban.jsx
│   │   ├── Statistiques.jsx
│   │   └── Profil.jsx
│   ├── App.jsx
│   └── index.css
└── package.json
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone <url_du_projet>
cd esmt_tasks
```

### 2. Backend Django

```bash
# Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate      # Windows

# Installer les dépendances
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers channels daphne pillow

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
daphne -p 8000 config.asgi:application
```

### 3. Frontend React

```bash
cd esmt_frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

---

## 🌐 URLs

| Interface     | URL                          |
|---------------|------------------------------|
| Django (HTML) | http://127.0.0.1:8000        |
| React         | http://localhost:5173        |
| API REST      | http://127.0.0.1:8000/api/   |
| Admin Django  | http://127.0.0.1:8000/admin/ |

---

## 👥 Comptes de Test

| Username      | Mot de passe | Rôle       |
|---------------|--------------|------------|
| prof_ada      | millionnaire | Professeur |
| etudiant_star | millionnaire | Étudiant   |
| etudiant_ngom | millionnaire | Étudiant   |
| prof_star     | millionnaire | Professeur |
| stark         | millionnaire | Étudiant   |
| adastar       | adastar      | Étudiant   |

---

## ✅ Fonctionnalités

### Authentification
- Inscription avec choix du rôle (Étudiant / Professeur)
- Connexion / Déconnexion
- JWT pour l'API React
- Session Django pour l'interface HTML

### Projets
- Créer, modifier, supprimer des projets
- Ajouter / retirer des membres
- Règle métier : un étudiant ne peut pas assigner un professeur

### Tâches
- Créer, modifier, supprimer des tâches
- Statuts : À faire / En cours / Terminé
- Priorités : Basse / Moyenne / Haute
- Assignation à un membre du projet
- Date limite avec indicateur de retard
- Filtres par statut et priorité

### Tableau Kanban
- Vue Kanban avec 3 colonnes
- Drag & drop (React uniquement)
- Changement de statut depuis Django

### Statistiques & Primes
- Taux de complétion par projet
- Graphiques Chart.js (donut)
- Prime 30 000 FCFA à 90% dans les délais
- Prime 100 000 FCFA à 100% dans les délais

### Chat en Temps Réel
- WebSockets avec Django Channels
- Messages persistants en base de données
- Disponible sur Django et React

### Notifications
- Alertes visuelles pour deadlines proches (3 jours)
- Alertes pour tâches en retard
- Notifications email via Gmail SMTP

### Autres
- Mode sombre / clair
- Recherche globale (projets + tâches)
- Page profil modifiable
- Dashboard analytique

---

## 🔌 API REST — Endpoints

| URL                           | Méthode            | Description           |
|-------------------------------|--------------------|-----------------------|
| `/api/auth/login/`            | POST               | Connexion JWT         |
| `/api/auth/register/`         | POST               | Inscription           |
| `/api/auth/me/`               | GET/PUT            | Profil utilisateur    |
| `/api/projets/`               | GET/POST           | Liste / Créer projets |
| `/api/projets/<pk>/`          | GET/PUT/DELETE     | Détail projet         |
| `/api/projets/<pk>/membres/`  | POST/DELETE        | Gestion membres       |
| `/api/projets/<pk>/taches/`   | GET/POST           | Tâches du projet      |
| `/api/taches/<pk>/`           | GET/PUT/DELETE     | Détail tâche          |
| `/api/taches/<pk>/statut/`    | POST               | Changer statut        |
| `/api/statistiques/`          | GET                | Stats + primes        |
| `/api/projets/<pk>/messages/` | GET                | Messages chat         |

---

## 🗃️ Modèles de Données

### User (accounts/models.py)
| Champ    | Type         | Description                  |
|----------|--------------|------------------------------|
| username | CharField    | Nom d'utilisateur unique     |
| email    | EmailField   | Adresse email                |
| password | CharField    | Mot de passe hashé           |
| role     | CharField    | `etudiant` ou `professeur`   |
| avatar   | ImageField   | Photo de profil (optionnel)  |

### Project (projects/models.py)
| Champ         | Type                  | Description             |
|---------------|-----------------------|-------------------------|
| id            | AutoField             | Identifiant unique      |
| titre         | CharField(200)        | Titre du projet         |
| description   | TextField             | Description             |
| createur      | ForeignKey(User)      | Créateur du projet      |
| membres       | ManyToManyField(User) | Membres du projet       |
| date_creation | DateTimeField         | Date de création (auto) |

### Task (tasks/models.py)
| Champ           | Type                | Description                    |
|-----------------|---------------------|--------------------------------|
| id              | AutoField           | Identifiant unique             |
| titre           | CharField(200)      | Titre de la tâche              |
| description     | TextField           | Description (optionnel)        |
| projet          | ForeignKey(Project) | Projet associé                 |
| assignee        | ForeignKey(User)    | Membre assigné (optionnel)     |
| statut          | CharField           | `todo`, `en_cours`, `termine`  |
| priorite        | CharField           | `basse`, `moyenne`, `haute`    |
| date_limite     | DateField           | Deadline (optionnel)           |
| date_creation   | DateTimeField       | Date de création (auto)        |
| date_fin_reelle | DateTimeField       | Date de fin réelle (optionnel) |

### Message (chat/models.py)
| Champ      | Type                |  Description        |
|------------|---------------------|---------------------|
| id         | AutoField           | Identifiant unique  |
| projet     | ForeignKey(Project) | Projet associé      |
| auteur     | ForeignKey(User)    | Auteur du message   |
| contenu    | TextField           | Contenu du message  |
| date_envoi | DateTimeField       | Date d'envoi (auto) |

---

## 📡 Exemples de Réponses API

**POST `/api/auth/login/`**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": { "id": 1, "username": "prof_ada", "role": "professeur" }
}
```

**GET `/api/projets/`**
```json
[
  {
    "id": 1,
    "titre": "Développement Application Mobile",
    "description": "Projet de développement d'une app mobile",
    "createur": 1,
    "membres": [1, 2, 3],
    "date_creation": "2026-01-15T10:00:00Z"
  }
]
```

**GET `/api/projets/1/taches/`**
```json
[
  {
    "id": 1,
    "titre": "Maquette UI",
    "statut": "en_cours",
    "priorite": "haute",
    "assignee": 2,
    "date_limite": "2026-03-01"
  }
]
```

**GET `/api/statistiques/`**
```json
[
  {
    "projet": "Développement Application Mobile",
    "total_taches": 5,
    "terminees_in_delais": 4,
    "taux": 80.0,
    "prime": 0
  }
]
```

**WebSocket `ws://127.0.0.1:8000/ws/chat/<projet_id>/`**
```json
{ "message": "Bonjour !", "username": "prof_ada" }
```



## 🎨 Design

- **Couleur principale** : `#c9547a` (rose)
- **Police** : Poppins (Google Fonts)
- **Background** : `#fdf6f9`
- **Cards** : border `#fce8f0`, border-radius `16px`
- **Boutons** : gradient `#e8748a → #c9547a`, border-radius `25px`
- **Mode sombre** : background `#13131f`, cards `#1e1e2e`

---

## 📧 Configuration Email

Dans `config/settings.py` :

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'an7983588@gmail.com'
EMAIL_HOST_PASSWORD = 'oygy vfsv vnlp abts'
```

---
Développé par Adama NGOM

Projet réalisé dans le cadre du cours de développement web à l'ESMT (École Supérieure Multinationale des Télécommunications).

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
EMAIL_HOST_USER = 'ton_email@gmail.com'
EMAIL_HOST_PASSWORD = 'ton_app_password_google'
```

---
Développé par Adama NGOM

Projet réalisé dans le cadre du cours de développement web à l'ESMT (École Supérieure Multinationale des Télécommunications).

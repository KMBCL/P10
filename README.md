# SoftDesk Support API

API REST de suivi de problèmes (projets, issues, commentaires), construite avec Django REST Framework et authentifiée par JWT.

## Prérequis

- Python 3.12
- Git
- Pipenv

```
pip install --user pipenv
```

## Installation

Cloner le dépôt :

```
git clone https://github.com/KMBCL/P10.git
cd P10
```

Installer les dépendances (versions figées par `Pipfile.lock`) dans un environnement virtuel `.venv` à la racine :

Windows (PowerShell) :

```
$env:PIPENV_VENV_IN_PROJECT = "1"
pipenv install --dev
```

macOS / Linux :

```
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

`--dev` ajoute les outils de développement (debug toolbar, flake8, stubs de typage). En production, `pipenv install` seul suffit, avec `DJANGO_DEBUG=False`.

Activer l'environnement :

```
pipenv shell
```

## Configuration

La clé secrète Django est lue dans `p10/.env` (fichier hors git). Sans elle, le serveur refuse de démarrer.

Copier le modèle :

```
cp p10/.env.example p10/.env
```

Générer une clé :

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

La coller dans `p10/.env` :

```
DJANGO_SECRET_KEY=<clé générée>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

`DJANGO_DEBUG=True` active le mode développement (debug toolbar, erreurs détaillées) ; absent ou `False`, le projet tourne en mode production.

## Lancement

Créer la base de données :

```
cd p10
python manage.py migrate
```

Démarrer le serveur :

```
python manage.py runserver
```

L'API est disponible sur http://127.0.0.1:8000/api/.

Sous Windows, `run.ps1` (à la racine) enchaîne `check`, `migrate` et `runserver` :

```
.\run.ps1
```

Compte administrateur (optionnel, pour http://127.0.0.1:8000/admin/) :

```
python manage.py createsuperuser
```

## Authentification

1. Créer un compte : `POST /api/user/` (accessible sans être connecté, âge minimum 15 ans).
2. Obtenir un token : `POST /api/token/` avec `username` et `password`.
3. Envoyer le token d'accès dans chaque requête :

```
Authorization: Bearer <access_token>
```

Le token d'accès expire après 5 minutes ; le renouveler via `POST /api/token/refresh/` avec le `refresh`.

## Endpoints

| Ressource | URL | Méthodes |
|---|---|---|
| Token | `/api/token/`, `/api/token/refresh/` | POST |
| Utilisateurs | `/api/user/` | POST (inscription), GET `?username=` (recherche) |
| Mon compte | `/api/user/{id}/` | GET, PUT, PATCH, DELETE |
| Projets | `/api/projects/` | GET, POST |
| Projet | `/api/projects/{id}/` | GET, PUT, PATCH, DELETE |
| Contributeurs | `/api/projects/{id}/contributors/` | GET, POST |
| Contributeur | `/api/projects/{id}/contributors/{id}/` | GET, DELETE |
| Issues | `/api/projects/{id}/issues/` | GET, POST |
| Issue | `/api/projects/{id}/issues/{id}/` | GET, PUT, PATCH, DELETE |
| Commentaires | `/api/projects/{id}/issues/{id}/comments/` | GET, POST |
| Commentaire | `/api/projects/{id}/issues/{id}/comments/{uuid}/` | GET, PUT, PATCH, DELETE |

Seuls les contributeurs d'un projet accèdent à ses ressources ; seul l'auteur d'une ressource peut la modifier ou la supprimer. Les listes sont paginées par 10 (`?page=N`).

Supprimer un projet supprime ses issues et leurs commentaires.

## Suppression de compte (RGPD)

`DELETE /api/user/{id}/` supprime le compte et ses participations aux projets. Les projets, issues et commentaires de l'utilisateur sont conservés mais anonymisés (`author` à `null`), et les issues qui lui étaient assignées passent à `assigned_to: null`. Une suppression en cascade détruirait le travail des autres contributeurs (leurs issues et commentaires dans ces projets).

Un contenu anonymisé reste lisible par les contributeurs mais n'est plus modifiable par personne. Limite connue : un projet dont l'auteur a supprimé son compte ne peut plus être modifié, supprimé, ni voir ses contributeurs gérés ; un transfert de propriété reste à prévoir.

## Qualité

Depuis la racine, avec les dépendances de développement :

```
flake8
```

Tests automatisés, depuis `p10/` :

```
python manage.py test -v 2
```

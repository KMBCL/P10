# SoftDesk Support API

API REST de suivi de problèmes (projets, issues, commentaires), construite avec Django REST Framework et authentifiée par JWT.

## Prérequis

- Python 3.12 (version imposée par le `Pipfile`)
- Git
- Pipenv

```
pip install --user pipenv
```

Si la commande `pipenv` n'est pas reconnue ensuite (cas fréquent sous Windows : le dossier des scripts utilisateur n'est pas dans le PATH), remplacer `pipenv` par `python -m pipenv` dans toutes les commandes ci-dessous.

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

Toutes les commandes suivantes s'exécutent dans cet environnement. À défaut de l'activer, préfixer chaque commande `python` ou `flake8` par `pipenv run` (exemple : `pipenv run python manage.py migrate`).

## Configuration

La clé secrète Django est lue dans `p10/.env` (fichier hors git). Sans elle, le serveur refuse de démarrer.

Copier le modèle, depuis la racine `P10` :

```
cp p10/.env.example p10/.env
```

(`cp` fonctionne dans PowerShell ; dans l'invite de commandes `cmd`, utiliser `copy p10\.env.example p10\.env`.)

Générer une clé :

```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Ouvrir `p10/.env` dans un éditeur et coller la clé après `DJANGO_SECRET_KEY=` :

```
DJANGO_SECRET_KEY=<clé générée>
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

`DJANGO_DEBUG=True` active le mode développement (debug toolbar, erreurs détaillées) ; absent ou `False`, le projet tourne en mode production.

## Lancement

Toutes les commandes `manage.py` s'exécutent depuis le dossier `p10` :

```
cd p10
```

Créer la base de données :

```
python manage.py migrate
```

Démarrer le serveur :

```
python manage.py runserver
```

L'API est disponible sur http://127.0.0.1:8000/api/. Arrêter le serveur avec `Ctrl+C`.

Compte administrateur (optionnel, pour http://127.0.0.1:8000/admin/) :

```
python manage.py createsuperuser
```

## Authentification

1. Créer un compte (sans être connecté) :

```
POST /api/user/
{
    "username": "alice",
    "password": "Mot2passe!",
    "age": 20,
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

L'âge minimum est de 15 ans. Le mot de passe doit faire au moins 8 caractères, avec au moins une lettre, un chiffre et un caractère spécial. Les deux consentements RGPD sont facultatifs et valent `false` s'ils sont absents.

2. Obtenir un token :

```
POST /api/token/
{
    "username": "alice",
    "password": "Mot2passe!"
}
```

La réponse contient un token d'accès `access` et un token de renouvellement `refresh`.

3. Envoyer le token d'accès dans l'en-tête de chaque requête :

```
Authorization: Bearer <access_token>
```

Le token d'accès expire après 5 minutes ; le renouveler via `POST /api/token/refresh/` avec `{"refresh": "<refresh_token>"}`. Le token de renouvellement expire après 1 jour.

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

Seuls les contributeurs d'un projet accèdent à ses ressources ; seul l'auteur d'une ressource peut la modifier ou la supprimer. L'auteur d'un projet en devient automatiquement contributeur, et lui seul peut ajouter ou retirer des contributeurs. Les listes sont paginées par 10 (`?page=N`).

Supprimer un projet supprime ses issues et leurs commentaires.

### Corps des requêtes

| Ressource | Champs | Valeurs possibles |
|---|---|---|
| Projet | `name`, `description`, `project_type` | `project_type` : `BACK_END` (défaut), `FRONT_END`, `IOS`, `ANDROID` |
| Contributeur | `user` (id de l'utilisateur, trouvé via `GET /api/user/?username=`) | |
| Issue | `name`, `description`, `status`, `priority`, `issue_type`, `assigned_to` | `status` : `TO_DO` (défaut), `IN_PROGRESS`, `FINISHED` ; `priority` : `LOW` (défaut), `MEDIUM`, `HIGH` ; `issue_type` : `BUG` (défaut), `TASK`, `FEATURE` ; `assigned_to` : id d'un contributeur du projet, facultatif |
| Commentaire | `description` | |

L'auteur, le projet et l'issue sont déduits du token et de l'URL : ils ne sont pas à envoyer.

## Suppression de compte (RGPD)

`DELETE /api/user/{id}/` supprime le compte et ses participations aux projets. Les projets, issues et commentaires de l'utilisateur sont conservés mais anonymisés (`author` à `null`), et les issues qui lui étaient assignées passent à `assigned_to: null`. Une suppression en cascade détruirait le travail des autres contributeurs (leurs issues et commentaires dans ces projets).

Un contenu anonymisé reste lisible par les contributeurs mais n'est plus modifiable par personne. Limite connue : un projet dont l'auteur a supprimé son compte ne peut plus être modifié, supprimé, ni voir ses contributeurs gérés ; un transfert de propriété reste à prévoir.

## Qualité

Avec les dépendances de développement installées (`--dev`).

Linter, depuis la racine `P10` :

```
flake8
```

Tests automatisés, depuis le dossier `p10` :

```
python manage.py test -v 2
```

## Fait

- [x] User, hérité de AbstractUser (age >= 16, can_be_contacted, can_data_be_shared)
- [x] Validateur de mot de passe personnalisé
- [x] UserSerializer
- [x] UserViewset (ModelViewSet : CRUD complet, à restreindre par permissions)
- [x] Migrations authentication
- [x] Modèles Project, Issue, Comment (UUID), Contributor (unique user/projet)
- [x] Serializers Project, Issue, Comment, Contributor
- [x] Validation : assigned_to doit être contributeur du projet
- [x] ModelViewSet Project (auteur + premier contributeur automatiques)
- [x] ModelViewSet Issue et Comment (auteur automatique)
- [x] URLs projects et authentication incluses dans les URLs principales
- [x] IsAuthenticated par défaut sur toute l'API

## Base de données

- [x] Corriger la valeur "FEATUR" de Issue.TypeTag.IMPROVEMENT (avant migration)
- [x] makemigrations projects + migrate
- [x] Vérifier dans l'admin ou le shell que les objets se créent correctement

## Authentification JWT

- [x] Installer djangorestframework-simplejwt (+ requirements)
- [x] Configurer DEFAULT_AUTHENTICATION_CLASSES (JWTAuthentication)
- [x] Routes token/ (obtention) et token/refresh/
- [x] Régler la durée de vie des tokens (SIMPLE_JWT)

## Utilisateurs / RGPD

- [x] Inscription : création de compte accessible sans être connecté (AllowAny via get_permissions)
- [x] Mot de passe en write_only et hashé à la création (create_user)
- [x] Mot de passe hashé aussi en modification (update() du serializer : set_password)
- [x] Appliquer AUTH_PASSWORD_VALIDATORS à l'inscription (validate_password dans le serializer)
- [x] Refuser l'inscription des moins de 16 ans (MinValueValidator du modèle, repris par le serializer)
- [ ] Message d'erreur personnalisé pour l'âge (constante dans constants.py)
- [x] Un utilisateur peut consulter et modifier son propre profil (consentements inclus)
- [ ] Droit à l'oubli : un utilisateur peut supprimer son compte (et ses données)
- [x] Un utilisateur ne peut pas modifier ou supprimer le compte d'un autre (IsSelf, has_object_permission → 403)
- [x] Liste complète des utilisateurs bloquée : list renvoie none() sans ?username= (get_queryset restreint à l'action list)
- [ ] Ne pas exposer de données sensibles dans la recherche ?username= (serializer allégé : id, username)

## Dette technique (à corriger)

- [x] ImportError : MIN_AWALLOWED_AGE_ERROR_MESSAGE importé mais absent de constants.py (import retiré)
- [ ] Remplacer l'import privé _SupportsHasPermission par un Protocol local
- [x] Supprimer les imports inutilisés de view.py
- [ ] Supprimer les imports inutilisés (projects/admin.py, projects/tests.py)
- [ ] flake8 E501 : permissions.py:9 (signature de has_object_permission à couper)
- [ ] Pyright : "Meta overrides symbol" sur les 5 serializers (configuration ou ignore)
- [ ] Pyright : typage de perform_create (BaseSerializer[Any] ou ignore ciblé)

## Contributors

- [ ] Vue Contributor : lister les contributeurs d'un projet
- [ ] Ajouter un contributeur à un projet (par l'auteur du projet)
- [ ] Retirer un contributeur d'un projet (par l'auteur du projet)
- [ ] Empêcher de retirer l'auteur du projet
- [ ] URLs Contributor

## Routes imbriquées (recommandé)

- [ ] projects/{id}/contributors/
- [ ] projects/{id}/issues/ (project injecté depuis l'URL, read_only dans le serializer)
- [ ] projects/{id}/issues/{id}/comments/ (issue injectée depuis l'URL)
- [ ] Retirer ou adapter les routes plates issues/ et comments/

## Permissions

- [ ] Projets : la liste ne montre que les projets dont l'utilisateur est contributeur (get_queryset)
- [ ] Projets : seul l'auteur peut modifier ou supprimer
- [ ] Issues : seuls les contributeurs du projet peuvent lire et créer
- [ ] Issues : seul l'auteur peut modifier ou supprimer
- [ ] Comments : seuls les contributeurs du projet peuvent lire et créer
- [ ] Comments : seul l'auteur peut modifier ou supprimer
- [x] Fichier authentication/permissions.py créé (IsSelf) : mécanisme has_permission / has_object_permission compris
- [ ] Permissions projects : IsAuthor, IsContributor (même mécanisme)

## Green code / performance

- [ ] Pagination globale (DEFAULT_PAGINATION_CLASS + PAGE_SIZE)
- [ ] select_related / prefetch_related dans les get_queryset
- [ ] Vérifier les requêtes avec la debug toolbar (éviter le N+1)
- [ ] Serializers allégés pour les listes (optionnel : list vs detail)

## Qualité et livraison

- [x] Fichier requirements.txt ou Pipfile à jour
- [ ] README : installation, lancement, endpoints
- [ ] flake8 et Pyright sans erreur
- [ ] Collection Postman couvrant tous les endpoints (cas autorisés et refusés)
- [ ] Vérifier chaque point du cahier des charges avant soutenance

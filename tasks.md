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
- [x] Droit à l'oubli : un utilisateur peut supprimer son compte et ses données (destroy du ModelViewSet + on_delete CASCADE)
- [x] Un utilisateur ne peut pas modifier ou supprimer le compte d'un autre (IsSelf, has_object_permission → 403)
- [x] Liste complète des utilisateurs bloquée : list renvoie none() sans ?username= (get_queryset restreint à l'action list)
- [x] Ne pas exposer de données sensibles dans la recherche ?username= (serializer allégé : id, username)

## Dette technique (à corriger)

- [x] ImportError : MIN_AWALLOWED_AGE_ERROR_MESSAGE importé mais absent de constants.py (import retiré)
- [ ] Remplacer l'import privé _SupportsHasPermission par un Protocol local
- [x] Supprimer les imports inutilisés de view.py
- [ ] Supprimer les imports inutilisés (projects/admin.py, projects/tests.py)
- [ ] Imports inutilisés : PermissionDenied (projects/views.py), Comment et Contributor (serializers/issue.py), Contributor (serializers/comment.py)
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

- [x] Projets : la liste ne montre que les projets dont l'utilisateur est contributeur (get_queryset)
- [x] Projets : seul l'auteur peut modifier ou supprimer (IsAuthor → 403 ; non-contributeur → 404)
- [x] Issues : seuls les contributeurs du projet peuvent lire (get_queryset) et créer/déplacer (IssueSerializer.validate → 400)
- [x] Issues : seul l'auteur peut modifier ou supprimer
- [x] Comments : seuls les contributeurs du projet peuvent lire (get_queryset) et créer (CommentSerializer.validate → 400)
- [x] Comments : seul l'auteur peut modifier ou supprimer
- [x] Fichier authentication/permissions.py créé (IsSelf) : mécanisme has_permission / has_object_permission compris
- [x] Permissions projects écrites : IsAuthor, IsProjectContributor, IsIssueContributor, IsCommentContributor (projects/permissions.py)
- [x] IsAuthor branché dans get_permissions des 3 viewsets (update/partial_update/destroy)
- [x] Scénarios vérifiés par script (APIClient, transaction annulée) le 2026-11-09 : 17/17 conformes
- [ ] IsProjectContributor / IsIssueContributor / IsCommentContributor inutilisés (le get_queryset couvre déjà) : supprimer ou brancher
- [ ] (Optionnel) Non-contributeur qui crée une issue/comment : 403 (PermissionDenied) plutôt que 400
- [ ] CommentSerializer : clé d'erreur "project" → "issue" (le champ soumis est issue)
- [ ] Factoriser is_contributor dupliqué dans IssueSerializer et CommentSerializer

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

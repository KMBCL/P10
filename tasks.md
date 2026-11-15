## Score d'audit (2026-11-09) : 74 / 100

## Fait

- [x] User, hérité de AbstractUser (age >= 16, can_be_contacted, can_data_be_shared)
- [x] Validateur de mot de passe personnalisé
- [x] UserSerializer
- [x] UserViewset (ModelViewSet : CRUD complet, restreint à son propre compte par get_queryset)
- [x] Migrations authentication
- [x] Modèles Project, Issue, Comment (UUID), Contributor (unique user/projet)
- [x] Serializers Project, Issue, Comment, Contributor
- [x] Validation : assigned_to doit être contributeur du projet (AssignableUserField, queryset = contributeurs du projet de l'URL)
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
- [ ] DÉCISION : CASCADE supprime aussi les issues/comments des autres contributeurs dans les projets de l'utilisateur supprimé → garder (et le justifier) ou anonymiser. Voir avec le mentor.
- [x] Un utilisateur ne peut ni voir, ni modifier, ni supprimer le compte d'un autre : get_queryset filtré sur pk=request.user → 404 (IsSelf supprimé, 2026-11-15)
- [x] Pas d'énumération des comptes : autre compte et compte inexistant → même 404 (vérifié 2026-11-15)
- [x] Liste complète des utilisateurs bloquée : list renvoie none() sans ?username= (get_queryset restreint à l'action list)
- [x] Ne pas exposer de données sensibles dans la recherche ?username= (serializer allégé : id, username)
- [x] Utilisateurs liés affichés comme objet {id, username} (UserListSerializer / UserRelatedField) : author, assigned_to, Contributor.user
- [x] assigned_to : id inexistant et id hors projet → même message « Utilisateur invalide pour ce projet. » (OWASP, énumération)

## Dette technique (à corriger)

- [x] ImportError : MIN_AWALLOWED_AGE_ERROR_MESSAGE importé mais absent de constants.py (import retiré)
- [x] ImportError : _SupportsHasPermission importé à l'exécution dans projects/views.py (n'existe que dans les stubs) → retiré, reste sous TYPE_CHECKING
- [x] ImportError : UsesQuerySet importé depuis rest_framework.generics (stub uniquement) → ligne retirée
- [ ] Règle à retenir : un nom qui n'existe que dans les stubs (_SupportsHasPermission, UsesQuerySet, _MT…) s'importe UNIQUEMENT sous `if TYPE_CHECKING:`
- [ ] Remplacer l'import privé _SupportsHasPermission par un Protocol local
- [ ] Pylance : user_id / author_id inconnus (FK annotées à la main) → annoter `user_id: int` / `author_id: int` dans les modèles, ou comparer instance.user == instance.project.author
- [ ] Pyright : perform_destroy(instance: Contributor) incompatible → `# pyright: ignore[reportIncompatibleMethodOverride]`
- [ ] flake8 (hors migrations, max-line-length 119) : 2 erreurs F401 restantes (2026-11-15)
- [x] Supprimer les imports inutilisés de view.py
- [ ] Supprimer les imports inutilisés (projects/admin.py, projects/tests.py) — ou enregistrer les modèles dans l'admin
- [x] Imports inutilisés : views.py, serializers/issue.py, serializers/comment.py, serializers/contributor.py
- [x] flake8 E501 : permissions.py (réécrit)
- [ ] Pyright : "Meta overrides symbol" sur les serializers (configuration ou ignore)
- [ ] Pyright : typage de perform_create (BaseSerializer[Any] ou ignore ciblé)
- [ ] Pylance : `routers.SimpleRouter` non exporté par rest_framework_nested → importer SimpleRouter depuis rest_framework.routers (projects/urls.py)
- [x] Commentaires # supprimés (2026-11-15)
- [ ] Docstrings à écrire. Y reprendre : project__author dans le select_related d'Issue, tri imposé par la pagination, http_method_names de ContributorViewSet, get_queryset de UserViewset = seule protection des comptes

## Contributors

- [x] ContributorViewSet + ContributorSerializer
- [x] URL imbriquée /api/projects/{project_pk}/contributors/
- [x] Non authentifié → 401 ; non-contributeur du projet → 403 (IsProjectContributor)
- [x] Doublon user/projet refusé → 400 (validate_user : project en read_only, DRF n'applique plus le UniqueTogetherValidator)
- [x] get_queryset filtré sur project_pk + contributeur
- [x] Ajout et suppression réservés à l'auteur du projet (IsProjectAuthor au niveau vue, sur project_pk → 403)
- [x] L'auteur ne peut pas se retirer de son projet (perform_destroy → 403)
- [x] Audit script 2026-11-09 (transaction annulée) : 18/19 conformes
- [x] FAILLE corrigée : PUT/PATCH bloqués (http_method_names → 405), l'auteur ne peut plus s'évincer par PATCH user
- [ ] Champ author sur Contributor (« chaque ressource hors utilisateur doit posséder un author ») ou justifier project.author

## Routes imbriquées

- [x] projects/{id}/contributors/
- [x] projects/{id}/issues/ (project injecté depuis l'URL, read_only dans le serializer)
- [x] projects/{id}/issues/{id}/comments/ (issue injectée depuis l'URL, appartenance au projet vérifiée → 404)
- [x] Routes plates issues/ et comments/ retirées
- [x] lookup_value_regex = r"\d+" sur Project et Issue (id non numérique → 404, pas 500)

## Permissions

- [x] Projets : la liste ne montre que les projets dont l'utilisateur est contributeur (get_queryset)
- [x] Projets : seul l'auteur peut modifier ou supprimer (IsAuthor → 403 ; non-contributeur → 404)
- [x] Issues : seuls les contributeurs du projet peuvent lire et créer (IsProjectContributor → 403)
- [x] Issues : seul l'auteur peut modifier ou supprimer
- [x] Comments : seuls les contributeurs du projet peuvent lire et créer (IsProjectContributor → 403)
- [x] Comments : seul l'auteur peut modifier ou supprimer
- [x] Mécanisme has_permission / has_object_permission compris
- [x] Permissions projects : IsAuthor, IsProjectContributor, IsProjectAuthor (projects/permissions.py) + AccessManager (projects/access.py)
- [x] IsAuthor branché dans get_permissions des viewsets (update/partial_update/destroy)
- [x] Scénarios vérifiés par script (APIClient, transaction annulée) le 2026-11-09 : 17/17 conformes
- [x] IsIssueContributor / IsCommentContributor supprimés
- [x] IsProjectAuthor réécrite au niveau vue (has_permission sur project_pk) pour couvrir create
- [x] Non-contributeur qui crée une issue/comment : 403 (permission) au lieu de 400 (serializer)
- [x] Validations de contributeur retirées des serializers (remplacées par les permissions)

## Green code / performance

- [x] Pagination globale (PageNumberPagination, PAGE_SIZE = 10) + order_by stable dans chaque get_queryset
- [x] select_related dans les get_queryset (aucun prefetch_related nécessaire : aucune relation many sérialisée)
- [x] Requêtes mesurées (CaptureQueriesContext) : nombre constant par endpoint, ex. liste issues 9 → 3
- [x] Serializer allégé pour la liste des issues (IssueListSerializer)

## Qualité et livraison

- [x] requirements.txt unique à la racine, à jour (Django gardé en 5.2 LTS ; djangorestframework-stubs 3.18 exige Django 6)
- [ ] README : installation, lancement, endpoints
- [ ] .env.example (DJANGO_SECRET_KEY obligatoire, sinon KeyError au démarrage)
- [ ] flake8 et Pyright sans erreur
- [ ] Tests automatisés des cas sensibles (404 hors projet, 403 non-auteur, assigned_to hors projet, comment sur issue d'un autre projet)
- [ ] Collection Postman couvrant tous les endpoints (cas autorisés et refusés) — listes désormais paginées : {count, next, previous, results}
- [ ] Vérifier chaque point du cahier des charges avant soutenance

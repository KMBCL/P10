## Fait

- [x] User, hérité de AbstractUser (age >= 16, can_be_contacted, can_data_be_shared)
- [x] Validateur de mot de passe personnalisé
- [x] UserSerializer
- [x] UserAPIView / UserViewset (lecture seule)
- [x] Migrations authentication
- [x] Modèles Project, Issue, Comment (UUID), Contributor (unique user/projet)
- [x] Serializers Project, Issue, Comment, Contributor
- [x] Validation : assigned_to doit être contributeur du projet
- [x] ModelViewSet Project (auteur + premier contributeur automatiques)
- [x] ModelViewSet Issue et Comment (auteur automatique)
- [x] URLs projects et authentication incluses dans les URLs principales
- [x] IsAuthenticated par défaut sur toute l'API

## Base de données

- [ ] Corriger la valeur "FEATUR" de Issue.TypeTag.IMPROVEMENT (avant migration)
- [ ] makemigrations projects + migrate
- [ ] Vérifier dans l'admin ou le shell que les objets se créent correctement

## Authentification JWT

- [ ] Installer djangorestframework-simplejwt (+ requirements)
- [ ] Configurer DEFAULT_AUTHENTICATION_CLASSES (JWTAuthentication)
- [ ] Routes token/ (obtention) et token/refresh/
- [ ] Régler la durée de vie des tokens (SIMPLE_JWT)

## Utilisateurs / RGPD

- [ ] Inscription : création de compte accessible sans être connecté (AllowAny)
- [ ] Mot de passe en write_only et hashé (set_password / create_user)
- [ ] Refuser l'inscription des moins de 16 ans (validation côté serializer)
- [ ] Un utilisateur peut consulter et modifier son propre profil (consentements inclus)
- [ ] Droit à l'oubli : un utilisateur peut supprimer son compte (et ses données)
- [ ] Un utilisateur ne peut pas modifier ou supprimer le compte d'un autre
- [ ] Ne pas exposer de données sensibles dans les listes d'utilisateurs

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
- [ ] Écrire les classes de permission dans un fichier permissions.py (has_permission / has_object_permission)

## Green code / performance

- [ ] Pagination globale (DEFAULT_PAGINATION_CLASS + PAGE_SIZE)
- [ ] select_related / prefetch_related dans les get_queryset
- [ ] Vérifier les requêtes avec la debug toolbar (éviter le N+1)
- [ ] Serializers allégés pour les listes (optionnel : list vs detail)

## Qualité et livraison

- [ ] Fichier requirements.txt ou Pipfile à jour
- [ ] README : installation, lancement, endpoints
- [ ] flake8 et Pyright sans erreur
- [ ] Collection Postman couvrant tous les endpoints (cas autorisés et refusés)
- [ ] Vérifier chaque point du cahier des charges avant soutenance

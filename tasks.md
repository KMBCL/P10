## Livraison

- [x] README : installation, lancement, endpoints + .env.example (DJANGO_SECRET_KEY obligatoire, sinon KeyError au démarrage)
- [x] Remplacer pip/requirements.txt par Pipenv ou Poetry (OCR + document sécurité), dépendances de dev séparées (django-stubs, flake8, types-PyYAML, debug-toolbar chargée seulement si DEBUG)
- [x] Âge minimum à 15 ans, pas 16 (document sécurité : « l'âge légal pour donner son consentement seul est de 15 ans » ; OCR : « moins de 15 ans » refusé) → MIN_ALLOWED_AGE = 15 + migration
- [x] Un seul niveau d'imbrication (OCR) : IssueSerializer imbrique project → author (2 niveaux) → retirer author de ProjectRelatedSerializer
- [ ] Champ author sur Contributor (« chaque ressource hors utilisateur doit posséder un author ») ou justifier project.author
- [ ] Tests automatisés des cas sensibles (404 hors projet, 403 non-auteur, assigned_to hors projet, comment sur issue d'un autre projet) et/ou collection Postman couvrant tous les endpoints (cas autorisés et refusés) — listes paginées : {count, next, previous, results}

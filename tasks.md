## Soutenance tasks

### Collection Postman (cas d'usage qui fonctionnent)

Un scénario enchaîné, token et id stockés en variables :

- [ ] Inscription d'Alice et de Bob
- [ ] Obtention du token d'Alice
- [ ] Alice crée un projet
- [ ] Alice ajoute Bob comme contributeur
- [ ] Alice crée une issue assignée à Bob
- [ ] Bob se connecte et commente l'issue
- [ ] Bob liste les issues du projet (pagination)
- [ ] Alice modifie son issue
- [ ] Refresh du token d'Alice
- [ ] Alice supprime son projet (cascade issues/commentaires)

### Tests automatisés (cas de refus) — `python manage.py test -v 2`

- [ ] Authentification : requête sans token → 401
- [ ] RGPD : inscription avec âge 14 → 400
- [ ] RGPD : consentements absents à l'inscription → `can_be_contacted` / `can_data_be_shared` à False
- [ ] Mot de passe trop faible (sans chiffre ou sans caractère spécial) → 400
- [ ] Comptes : lire ou modifier le compte d'un autre utilisateur → 404
- [ ] Accès projet : un non-contributeur ne voit ni le projet, ni ses issues, ni ses commentaires
- [ ] Auteur : un contributeur modifie ou supprime le projet, l'issue ou le commentaire d'un autre → 403
- [ ] Contributeurs : un non-auteur du projet ajoute ou retire quelqu'un → 403
- [ ] Contributeurs : retirer l'auteur du projet → 403
- [ ] Contributeurs : ajouter deux fois le même utilisateur → 400
- [ ] Assignation à un utilisateur hors projet → 400, même message qu'un id inexistant (anti-énumération)
- [ ] Imbrication d'URL : commenter une issue via l'id d'un autre projet → 404
- [x] RGPD : suppression du compte → compte et contributions supprimés, contenu anonymisé (author = null)

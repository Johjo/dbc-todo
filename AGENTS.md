# Règles de collaboration

## Interdits
- Ne jamais push.
- Ne jamais rollback (reset, revert, amend) : c'est l'humain qui décide.

## Workflow de développement (git-gamble / TDD)
Une seule étape à la fois, validée avant de passer à la suivante :

1. Proposer l'étape et attendre la validation de l'humain.
2. Écrire UN SEUL test (rouge). L'humain valide avec `make red`.
3. Faire passer le test. L'agent valide avec `make green`.
4. Discuter du résultat avant l'étape suivante.

## Conventions du dépôt
- Fichiers en CRLF.
- Un commit par fonctionnalité, message au format `feat: #N ...` / `test: #N ...`.

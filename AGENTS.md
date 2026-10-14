# Règles de collaboration

## Interdits
- Ne jamais push.
- Ne jamais rollback (reset, revert, amend) : c'est l'humain qui décide.

## Workflow de développement (git-gamble / TDD)
- Maintenir une todo list pour que l'humain suive l'avancement.
- Une modification à la fois, chacune validée par un pari git-gamble :
  1. Écrire le test (rouge) : `make red MESSAGE="..."`.
  2. Faire passer le test : `make green MESSAGE="..."`.
- Après chaque modification, discuter du résultat avant la suivante.
- En cas de doute, poser une question plutôt que deviner.

## Conventions du dépôt
- Fichiers en LF (garanti par .gitattributes).
- Un commit par modification, message au format `feat: ...` / `test: ...` / `chore: ...`.
- Les erreurs métier sont des dataclasses retournées dans un `Result`, jamais d'exception.

---
description: Review les changements git avant commit — qualité, bugs, sécurité
---

# Review

## Contexte

- Branche : !`git branch --show-current`
- Changements staged : !`git diff --cached --stat`
- Changements unstaged : !`git diff --stat`
- Diff complet : !`git diff --cached`
- Diff unstaged : !`git diff`

## Checklist de review

Analyse chaque fichier modifié et vérifie :

**Qualité du code**
- Nommage clair et cohérent avec le reste du projet
- Pas de `any` TypeScript — `unknown` ou type précis
- Pas de `console.log` ou code commenté oublié
- Fonctions courtes et focalisées (une responsabilité)
- Pas d'abstraction prématurée ou sur-ingénierie

**Bugs potentiels**
- Gestion des cas limites (null, undefined, tableau vide)
- Gestion des erreurs async (try/catch, .catch())
- Pas de mutation d'état non intentionnelle

**Sécurité**
- Pas de secrets ou credentials dans le code
- Entrées utilisateur validées avant utilisation
- Pas d'injection possible (SQL, XSS, etc.)

**Tests**
- Le code modifié a des tests associés
- Les cas d'erreur sont couverts

## Format de sortie

Classe par priorité :

**Critique** — doit être corrigé avant commit (bug, sécurité)
**Avertissement** — amélioration recommandée
**Suggestion** — optionnel, nice-to-have

Si rien à signaler : confirme que le code est propre et prêt pour commit.

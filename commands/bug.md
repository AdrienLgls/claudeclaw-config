---
description: Investiguer et corriger un bug de manière structurée
---

# Bug Fix

## Bug à investiguer

$ARGUMENTS

Si aucune description fournie, demande à l'utilisateur de décrire le bug avant de continuer.

## Workflow

### 1. Comprendre

Avant tout code, répondre à ces questions :
- Quel est le comportement attendu ?
- Quel est le comportement actuel ?
- Dans quelles conditions le bug se reproduit-il ?

Cherche des indices : logs, messages d'erreur, stack trace.

### 2. Reproduire

Trouve ou écris un test minimal qui reproduit le bug.
Ce test DOIT échouer avant le fix.

YOU MUST: ne pas passer à l'étape suivante sans avoir reproduit le bug.

### 3. Root cause

Remonte à la source du problème — ne pas corriger le symptôme, corriger la cause.
- Lis les fichiers concernés
- Trace l'exécution depuis l'entrée jusqu'à l'erreur
- Identifie exactement la ligne ou logique fautive

### 4. Plan de fix

Liste les fichiers à modifier et les changements à faire.
Valide le plan avant de coder.

### 5. Implémenter

Applique le fix minimal — ne rien changer au-delà du nécessaire.

### 6. Vérifier

- Le test de reproduction passe maintenant
- Les tests existants passent toujours
- `pnpm typecheck && pnpm lint` au vert

### 7. Commit

Message format : `fix(scope): description du bug corrigé`

---
description: Initialise un nouveau projet avec CLAUDE.md et structure de base
---

# Nouveau projet

Nom du projet : $ARGUMENTS

Si aucun nom fourni, demande-le avant de continuer.

## Etape 1 — Choisir le type de projet

Demande à l'utilisateur :
1. Type : T3 Stack (Next.js + TypeScript + Tailwind + tRPC + Prisma + NextAuth) ou MERN ?
2. Description : En une phrase, à quoi sert ce projet ?
3. Features principales : Les 3-5 features du MVP

Attends la réponse avant de continuer.

## Etape 2 — Initialiser le projet

Si T3 :
```bash
pnpm create t3-app@latest [nom-projet]
```

Si MERN :
```bash
mkdir [nom-projet] && cd [nom-projet] && pnpm init
```
Puis créer : src/, src/routes/, src/models/, src/controllers/, src/middleware/

## Etape 3 — Créer le CLAUDE.md du projet

Crée un fichier CLAUDE.md à la racine du projet avec les sections suivantes adaptées aux réponses :
- Nom et description du projet
- Stack avec les versions
- Commandes pnpm (dev, build, test, lint, typecheck)
- Architecture (structure des dossiers)
- Features MVP à implémenter
- Règles spécifiques au projet

## Etape 4 — Setup Git

```bash
git init
git add .
git commit -m "chore: init project"
```

## Etape 5 — Résumé

Affiche :
- Le CLAUDE.md créé
- La commande pour démarrer le projet
- Les prochaines étapes recommandées pour le MVP

---
name: software-architecture
description: Guide for quality focused software architecture. Use when designing architecture, writing code, or analyzing code structure.
---

# Software Architecture

Based on Clean Architecture and Domain Driven Design principles.

## General Principles

- **Early return pattern**: Always use early returns over nested conditions
- Avoid code duplication through reusable functions and modules
- Decompose long components (>80 lines) into smaller ones
- Files >200 lines should be split
- Use arrow functions when possible

## Library-First Approach

**ALWAYS search for existing solutions before writing custom code:**
- Check npm for existing libraries
- Evaluate existing services/SaaS solutions
- Consider third-party APIs for common functionality

**When custom code IS justified:**
- Specific business logic unique to the domain
- Performance-critical paths
- Security-sensitive code requiring full control
- When existing solutions don't meet requirements after thorough evaluation

## Clean Architecture & DDD

- Follow domain-driven design and ubiquitous language
- Separate domain entities from infrastructure concerns
- Keep business logic independent of frameworks
- Define use cases clearly and keep them isolated

## Naming Conventions

- **AVOID** generic names: `utils`, `helpers`, `common`, `shared`
- **USE** domain-specific names: `OrderCalculator`, `UserAuthenticator`, `InvoiceGenerator`
- Follow bounded context naming patterns
- Each module should have a single, clear purpose

## Separation of Concerns

- Do NOT mix business logic with UI components
- Keep database queries out of controllers
- Maintain clear boundaries between contexts

## Anti-Patterns to Avoid

- **NIH Syndrome:** Don't build custom auth when Auth0/Supabase exists
- **Generic Naming:** `utils.js` with 50 unrelated functions
- **Deep Nesting:** Max 3 levels
- **God Functions:** Keep functions focused, under 50 lines
- Every line of custom code is a liability needing maintenance, testing, and documentation

## Code Quality

- Proper error handling with typed catch blocks
- Break down complex logic into smaller, reusable functions
- Keep functions focused and under 50 lines when possible
- Keep files focused and under 200 lines when possible

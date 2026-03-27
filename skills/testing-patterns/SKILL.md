---
name: testing-patterns
description: Testing patterns and strategies for JavaScript/TypeScript apps. Use when writing tests, setting up test frameworks, or improving test coverage. Triggers on "test", "testing", "vitest", "jest", "coverage", "mock", "e2e", "integration test".
user_invocable: true
---

# Testing Patterns

## Test Pyramid

```
        /  E2E  \        ← Few, slow, expensive (Playwright/Cypress)
       /----------\
      / Integration \     ← Some, moderate (Supertest + real DB)
     /----------------\
    /    Unit Tests     \  ← Many, fast, cheap (Vitest/Jest)
```

**Rule:** 70% unit, 20% integration, 10% E2E.

## Framework Selection

| Stack | Unit/Integration | E2E |
|-------|-----------------|-----|
| Vite + React | Vitest + Testing Library | Playwright |
| Next.js | Vitest + Testing Library | Playwright |
| Express API | Vitest + Supertest | - |
| MongoDB | Vitest + mongodb-memory-server | - |

## Unit Test Patterns

### Arrange-Act-Assert (AAA)
```javascript
test('calculates total with tax', () => {
  // Arrange
  const items = [{ price: 100 }, { price: 200 }]
  const taxRate = 0.15

  // Act
  const total = calculateTotal(items, taxRate)

  // Assert
  expect(total).toBe(345)
})
```

### Test naming: `should [expected behavior] when [condition]`
```javascript
test('should return 401 when token is expired', ...)
test('should create user when all fields are valid', ...)
test('should throw when email is already taken', ...)
```

### What to test in a function:
1. Happy path (normal input → expected output)
2. Edge cases (empty array, null, 0, negative numbers)
3. Error cases (invalid input → proper error)
4. Boundary values (min, max, off-by-one)

## Integration Test Patterns (Express + MongoDB)

```javascript
import { beforeAll, afterAll, describe, test, expect } from 'vitest'
import supertest from 'supertest'
import { MongoMemoryServer } from 'mongodb-memory-server'
import { app } from '../src/app'

let mongod
let request

beforeAll(async () => {
  mongod = await MongoMemoryServer.create()
  process.env.MONGODB_URI = mongod.getUri()
  request = supertest(app)
})

afterAll(async () => {
  await mongod.stop()
})

describe('POST /api/users', () => {
  test('should create user with valid data', async () => {
    const res = await request
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'Str0ng!Pass' })

    expect(res.status).toBe(201)
    expect(res.body.email).toBe('test@example.com')
    expect(res.body).not.toHaveProperty('password')
  })

  test('should return 400 with invalid email', async () => {
    const res = await request
      .post('/api/users')
      .send({ email: 'not-an-email', password: 'Str0ng!Pass' })

    expect(res.status).toBe(400)
  })
})
```

## React Component Test Patterns

```javascript
import { render, screen, fireEvent } from '@testing-library/react'
import { UserProfile } from './UserProfile'

test('should display user name', () => {
  render(<UserProfile user={{ name: 'Alice' }} />)
  expect(screen.getByText('Alice')).toBeInTheDocument()
})

test('should call onEdit when edit button clicked', () => {
  const onEdit = vi.fn()
  render(<UserProfile user={{ name: 'Alice' }} onEdit={onEdit} />)
  fireEvent.click(screen.getByRole('button', { name: /edit/i }))
  expect(onEdit).toHaveBeenCalledOnce()
})
```

## What NOT to Test
- Third-party library internals
- Private implementation details (test behavior, not implementation)
- Trivial getters/setters
- Framework code (React rendering, Express routing)
- Console.log output

## Anti-Patterns
- **Mocking everything** — tests pass but production breaks
- **Testing implementation** — breaks on every refactor
- **No assertions** — test runs but checks nothing
- **Shared mutable state** — tests depend on execution order
- **Snapshot overuse** — `toMatchSnapshot()` on everything = meaningless tests

## Setup Checklist (New Project)
1. Install: `pnpm add -D vitest @testing-library/react @testing-library/jest-dom`
2. Configure `vitest.config.js` with proper paths and environment
3. Add `"test": "vitest"` and `"test:coverage": "vitest --coverage"` to package.json
4. Create first test to verify setup works
5. Add test command to CI pipeline

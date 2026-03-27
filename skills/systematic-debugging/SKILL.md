---
name: systematic-debugging
description: Structured 4-phase debugging methodology. Use when investigating bugs, errors, crashes, or unexpected behavior. Triggers on "debug", "investigate", "root cause", "why does", "broken", "ne marche pas".
user_invocable: true
---

# Systematic Debugging

## Phase 1: Reproduce
Before anything else, reproduce the bug reliably.

1. Get exact steps to reproduce (user input, API call, test case)
2. Confirm you can trigger the bug consistently
3. Note the exact error message, stack trace, or unexpected output
4. Identify: does it happen always, intermittently, or under specific conditions?

**Output:** A minimal reproduction case (test, curl command, or steps).

## Phase 2: Isolate
Narrow down where the bug lives.

1. **Binary search the codebase** — comment out halves to find the offending module
2. **Check recent changes** — `git log --oneline -20`, `git diff HEAD~5`
3. **Trace the data flow** — follow input → processing → output, find where it diverges
4. **Check boundaries** — API responses, DB queries, env vars, config files
5. **Simplify** — remove middleware, plugins, wrappers until the bug disappears, then add back one by one

**Output:** The specific file, function, and line range where the bug originates.

## Phase 3: Fix
Apply the minimal correct fix.

1. Write a failing test that captures the bug
2. Fix the root cause (not symptoms)
3. Verify the test passes
4. Check for similar patterns elsewhere (`grep` for the same anti-pattern)
5. Ensure no regressions — run the full test suite

**Anti-patterns to avoid:**
- Shotgun debugging (changing random things hoping it works)
- Fixing symptoms instead of root cause
- Adding try/catch to silence errors
- "It works on my machine" without understanding why

## Phase 4: Verify & Prevent
Make sure it stays fixed.

1. The failing test from Phase 3 now passes
2. Run full test suite — no regressions
3. Consider: should this be caught by linting, types, or CI?
4. Document if the root cause was non-obvious

## Debugging Toolkit

| Technique | When to use |
|-----------|------------|
| `console.log` / breakpoints | Tracing data flow |
| `git bisect` | "It used to work" — find the breaking commit |
| `git stash` + test | "Is it my changes?" |
| Network tab / curl | API issues |
| DB queries direct | Data integrity issues |
| `strace` / `ltrace` | System-level issues |
| Rubber duck | When you're stuck after 15 min |

## Rules
- NEVER guess. Always verify with evidence.
- If stuck for >10 minutes on one approach, switch techniques.
- The bug is always logical — computers don't have opinions.
- If the fix is more than 10 lines, you might be fixing the wrong thing.

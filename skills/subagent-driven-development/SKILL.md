---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks - dispatches fresh subagent per task with code review between tasks, enabling fast iteration with quality gates
---

# Subagent-Driven Development

Create and execute plans by dispatching a fresh subagent per task, with code review after each.

**Core principle:** Fresh subagent per task + review between tasks = high quality, fast iteration.

## When to Use

- 3+ independent issues that can be investigated without shared state
- Executing multi-step implementation plans
- Parallel investigation of unrelated failures

## Sequential Execution

### 1. Load Plan
Read plan file, create TodoWrite with all tasks.

### 2. Execute Task with Subagent

For each task, dispatch a fresh subagent:
```
Task tool (general-purpose):
  description: "Implement Task N: [task name]"
  prompt: |
    You are implementing Task N from [plan-file].
    1. Implement exactly what the task specifies
    2. Write tests (following TDD if applicable)
    3. Verify implementation works
    4. Commit your work
    5. Report back: What you implemented, tested, files changed, any issues
```

### 3. Review Subagent's Work

Dispatch code-reviewer subagent on the diff between commits.

### 4. Apply Review Feedback

- Fix Critical issues immediately
- Fix Important issues before next task
- Note Minor issues
- Dispatch follow-up subagent if needed

### 5. Mark Complete, Next Task

Repeat steps 2-5 for each task.

### 6. Final Review

After all tasks, dispatch final code-reviewer reviewing entire implementation.

## Parallel Execution

When tasks are independent (different files, different subsystems):

### 1. Identify Independent Domains
Group by what's broken or what's being built.

### 2. Dispatch in Parallel
One agent per independent problem domain. Let them work concurrently.

### 3. Review and Integrate
- Read each summary
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Good Agent Prompts

1. **Focused** - One clear problem domain
2. **Self-contained** - All context needed
3. **Specific about output** - What should the agent return?
4. **Constrained** - Don't change unrelated code

## Red Flags

**Never:**
- Skip code review between tasks
- Proceed with unfixed Critical issues
- Dispatch multiple implementation subagents on same files (conflicts)
- Implement without reading the plan task

**If subagent fails:** Dispatch fix subagent with specific instructions. Don't try to fix manually (context pollution).

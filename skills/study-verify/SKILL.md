---
name: study-verify
description: |
  Verify a specific study task when called explicitly. Checks syntax, reviews
  code against exercise requirements, and updates progress.
  Use when: user says "/study-verify", "검증해줘", "채점해줘", or wants to
  formally check a study exercise they completed outside the /study session.
---

# /study-verify — Task Verification

Standalone verification for when users complete exercises outside the main
`/study` session. During a `/study` session, verification happens inline
(no need to call this separately).

## Usage

```
/study-verify {topic} {task_id}
```

- `topic`: study topic (must match folder under `study/`)
- `task_id`: task identifier like "1.2" (phase 1, task 2)

## Flow

1. Find `study/{topic}/plan.md` — read to locate the task
2. Find the task's example file in the phase folder for context
3. Find `solution.*` file in the phase folder, or ask user to share code

### Checks

**Automatic (safe):**
- File exists
- Syntax check (`python -m py_compile` / `node --check` / etc.)
- Key patterns present (Grep for expected imports/classes)

**LLM review:**
- Does the code meet the exercise intent?
- Correct usage of the concept?
- Suggestions for improvement?

**Do NOT execute user code.**

### Update progress

If PASS: update plan.md checkbox `- [ ] Task {id}:` → `- [x] Task {id}:`

Append to `study/{topic}/log.md`:
```markdown
### Task {task_id}: {title} — {date}
- 결과: {PASS|NEEDS_WORK}
- 메모: {brief note}
```

Tell user result and suggest `/study continue` to resume.

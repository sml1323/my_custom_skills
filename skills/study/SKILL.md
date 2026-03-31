---
name: study
description: |
  Interactive hands-on learning skill. Teaches any library or concept through
  a 1:1 tutoring style: small tasks one at a time, concept + example first,
  then user implements while asking questions, then verify and move on.
  Two modes: "concept" for learning a new library from zero, "codebase" for
  understanding and improving existing code.
  Use this skill when: the user says "study", "learn", "배우고 싶어", "학습",
  "공부", wants to understand a library or framework, asks "how does X work",
  wants to understand existing code, says "이 코드 분석해줘" or "코드 이해하고 싶어",
  or says "/study". Also trigger when users mention wanting to prepare for
  interviews about a specific technology, or want to deeply understand a codebase
  before making changes.
---

# /study — Interactive Hands-On Learning

A 1:1 tutoring skill with two modes. Walks through small tasks one at a time:

```
개념/코드 설명 → 예제 보기 → 사용자 구현 (질문하며 진행) → 확인 → 다음 task
```

## Argument Parsing

```
/study concept {topic}[@version] [--phases N]   # 새 라이브러리/개념 학습
/study codebase {target_path}                    # 기존 코드 이해 + 고도화
/study list                                      # 진행 현황
/study continue                                  # 이어서 진행
```

- `concept`: Learn a new library/concept from zero to applied
- `codebase`: Understand existing code, then modify/improve it
- `list`: Show all topics with progress
- `continue`: Resume from where you left off

If just `/study` with no arguments, ask what they want to learn.

---

## Mode: Concept

For learning a new library or concept from scratch. Follows a tutorial-style
progression from basics to application.

### Setup (Concept)

**1. Check existing session:** If `study/{topic}/plan.md` exists, resume.

**2. Documentation source:**
- Try context7 first (`mcp__context7__resolve-library-id`)
- If `@version` specified, use matching version ID
- Fallback: WebSearch → LLM knowledge (limit 2 phases + warning)

**3. File extension:** Python→`.py` | JS/TS→`.ts` | Go→`.go` | Rust→`.rs`

**4. Create structure:**
```bash
mkdir -p study/{topic}/references
```
Fetch docs for phase 1 only (lazy). Save to `study/{topic}/references/official-docs.md`.

**5. Generate plan.md** using the plan template below, with:
- `> 모드: Concept`
- Phase progression: basics → core patterns → advanced/applied
- Last phase connects to user's actual project
- Each task = one small concept (~5-10 min)

**6. Start Task 1.1 immediately** — do NOT create all files upfront.

### Task Content (Concept)

In the learning loop, concept mode tasks work like this:
- **Concept step:** Explain from official docs, 한국어 + 영어 용어
- **Example step:** Minimal working example from official docs
  - Save to `study/{topic}/phase-{N}-{name}/task-{M}-example.{ext}`
- **Exercise step:** Modify/extend the example ("X를 Y로 바꿔보세요")
- **Verify step:** Syntax check + LLM review against exercise requirements

---

## Mode: Codebase

For understanding existing code deeply enough to modify and improve it.
Unlike concept mode's tutorial style, this is code reading + analysis + modification.

### Setup (Codebase)

**1. Validate target_path:**
```bash
ls {target_path} 2>/dev/null
```
If path doesn't exist, tell user and stop.

**2. Scan target files:**
Find all source files under target_path recursively. Apply limits:
- Max 50 files OR 10k total lines, whichever is reached first
- If exceeded, tell user: "파일이 너무 많습니다. 범위를 좁혀주세요."
- Count files and lines to report scope

**3. Analyze code structure:**
Read the files to understand:
- Directory structure and file roles
- Key classes, functions, entry points
- Dependencies (imports, packages)
- Patterns used (e.g., MVC, event-driven, pipeline)
- Existing tests (`tests/`, `test_*.py`, etc.)
- Existing lint/format config (`.flake8`, `pyproject.toml`, etc.)

**4. Detect languages and frameworks:**
Determine file extensions and frameworks from imports/configs.
Look up relevant documentation via context7 or WebSearch for the libraries used.

**5. Create structure:**
```bash
mkdir -p study/{topic}/references
```

Use the directory name or a descriptive slug as `{topic}` (e.g., `agent` for `src/agent/`).
Save a code structure summary to `study/{topic}/references/code-overview.md`.

**6. Generate plan.md** using the plan template below, with:
- `> 모드: Codebase`
- `> 대상: {target_path}`
- Phase progression for codebase understanding:

```
Phase 1: 구조 파악 (Structure)
  - Task 1.1: 디렉토리 구조와 파일 역할 파악
  - Task 1.2: 핵심 데이터 흐름 추적
  - Task 1.3: 의존성과 외부 라이브러리 이해

Phase 2: 패턴 이해 (Patterns)
  - Task 2.1: 핵심 디자인 패턴 분석
  - Task 2.2: 사용된 라이브러리의 관용적 사용법 이해
  - Task 2.3: 에러 처리와 edge case 전략 분석

Phase 3: 수정과 확장 (Modification)
  - Task 3.1: 기존 기능 수정 과제
  - Task 3.2: 새 기능 추가 과제
  - Task 3.3: 테스트 작성 과제
```

Adapt tasks based on what you found in the actual code.

**7. Start Task 1.1 immediately.**

### Task Content (Codebase)

In the learning loop, codebase mode tasks work differently:

- **Concept step:** Explain the relevant code section
  - Show actual code from the project with inline annotations (한국어 주석)
  - Explain the pattern/architecture being used
  - Reference official docs for the libraries involved

- **Example step:** Instead of a new example, show annotated excerpts
  - Pull relevant code snippets from target_path
  - Add 한국어 inline comments explaining each section
  - Save annotated version to `study/{topic}/phase-{N}-{name}/task-{M}-annotated.{ext}`

- **Exercise step:** Tasks that test real understanding
  - Phase 1 exercises: "이 함수의 실행 흐름을 설명해보세요", "이 코드의 입출력을 정리해보세요"
  - Phase 2 exercises: "이 패턴이 사용된 이유를 설명하고, 대안을 제시해보세요"
  - Phase 3 exercises: actual code modifications — "이 기능을 X로 수정해보세요", "Y 기능을 추가해보세요"

- **Verify step:** Use existing project infrastructure when available
  - If tests exist: suggest running `pytest {test_file}` to verify changes
  - If linter exists: suggest running lint to check code quality
  - For explanation tasks: LLM evaluates the user's explanation for accuracy
  - For code changes: LLM reviews the diff against exercise requirements

---

## The Learning Loop (shared, both modes)

This is the core interaction. Run it for each task, one at a time.

### Step 1: Concept (teach)

Explain the concept for this task:
- 한국어로 설명, 영어 기술 용어 병기
- 짧고 명확하게 (3-5 문장)
- 왜 이게 필요한지, 어떤 문제를 해결하는지
- **Concept mode:** reference official docs
- **Codebase mode:** anchor to specific files and symbols in the project.
  Always name the file path and function/class before generalizing.

### Step 2: Example (show)

Show ONE minimal working example or annotated code snippet:
- **Concept mode:** Minimal example from official docs with 한국어 주석
- **Codebase mode:** Annotated excerpt from the actual project code
- **Create the phase directory before saving** (it won't exist yet):
  ```bash
  mkdir -p study/{topic}/phase-{N}-{name}
  ```
- Save to phase folder for reference
- Cap at one example. No variations or "bonus" examples unless user asks.

### Step 3: Exercise (do)

Give the user ONE small, concrete task with clear completion criteria.
Then say: **"구현해보세요. 모르는 부분이 있으면 언제든 질문하세요."**

**Then STOP. Do not continue. Wait for user response.**
Do not preview future tasks, suggest multi-part exercises, or pre-solve anything.

### Step 4: Assist (interactive — hint escalation)

While the user works, follow this escalation ladder:
1. **질문 답변** — answer conceptual questions about the current task
2. **힌트** — if stuck, give a directional hint ("~를 살펴보세요")
3. **좁은 힌트** — still stuck, narrow it ("~함수의 ~파라미터를 확인해보세요")
4. **부분 스캐폴드** — show partial structure without the answer
5. **전체 설명** — only if explicitly asked or after 3+ failed attempts

Never jump straight to the answer. Each level should be tried before the next.
Only answer questions about the CURRENT task. Do not discuss future tasks.

Stay here until the user says done or asks to verify.

### Step 5: Verify (check)

When the user is done, apply mode-specific verification:

**Concept mode verification:**
- Syntax check: `python -m py_compile` or equivalent
- Key imports/patterns present (Grep)
- LLM review: does the code meet exercise requirements? Correct API usage?

**Codebase mode verification:**
- Anchor to specific files: reference exact file paths and line numbers
- If explanation task: evaluate accuracy against actual code (re-read the source)
- If modification task: suggest running existing tests (`pytest {test_file}`)
- If linter exists: suggest running lint
- LLM review: does the change match exercise intent? Any side effects?

**Do NOT auto-execute user code in either mode.**

**Feedback (concise, in chat):**
```
✅ Task {N}.{M} 완료!
- 잘한 점: {specific positive}
- 팁: {one improvement if any}
```

### Step 6: Record & Next

Update plan.md: `- [ ] Task {N}.{M}:` → `- [x] Task {N}.{M}:`

Append to `study/{topic}/log.md`:
```markdown
### Task {N}.{M}: {title} — {YYYY-MM-DD}
- 결과: PASS
- 메모: {one-line summary}
```

Then immediately present the next task.

Phase complete → brief summary:
```
📋 Phase {N} 완료!
배운 것: {2-3 bullet points}
다음: Phase {N+1} — {title}
```

For next phase, lazy-fetch new docs (concept) or analyze next code section (codebase).

ALL phases complete → generate `study/{topic}/summary.md` and congratulate.

---

## Plan Template

Both modes use this format. The checkbox format must be precise for Edit tool updates.

```markdown
# {Topic} 학습 계획

> 생성일: {YYYY-MM-DD}
> 모드: {Concept | Codebase}
> 문서 소스: {context7 | WebSearch | LLM 내장 지식}
> 대상: {target_path — codebase mode only}

## Phase 1: {phase_title}

- [ ] Task 1.1: {description}
- [ ] Task 1.2: {description}
- [ ] Task 1.3: {description}

## Phase 2: {phase_title}

- [ ] Task 2.1: {description}
- [ ] Task 2.2: {description}
- [ ] Task 2.3: {description}

## Phase 3: {phase_title}

- [ ] Task 3.1: {description}
- [ ] Task 3.2: {description}
- [ ] Task 3.3: {description}
```

---

## /study list

Scan `study/` directory. For each topic with plan.md:
- Read mode from header (`> 모드:` line)
- Count total/completed tasks
- Show progress:

```
📚 학습 현황
────────────────────────────────
langgraph    [Concept]  ██████░░░░  6/9 tasks (Phase 2, Task 2.3)
agent        [Codebase] ████░░░░░░  4/9 tasks (Phase 2, Task 2.1)
fastapi      [Concept]  ██████████  9/9 tasks ✓ 완료
```

## /study continue

Read plan.md, find first `- [ ]` task, resume the learning loop from Step 1.

---

## Output Contract (per task)

Each task interaction produces EXACTLY this sequence, then stops:
1. **Goal** — one sentence: what the user will learn
2. **Concept** — 3-5 sentences explaining the idea
3. **Example** — one minimal code snippet or annotated excerpt
4. **Exercise** — one concrete task with clear completion criteria
5. **STOP** — wait for user

**Prohibited during a task:**
- Previewing future tasks ("다음에는 ~를 배울 거예요")
- Multi-part exercises ("추가로 ~도 해보세요")
- Pre-solving the exercise
- Broad repo tours (codebase mode — stay anchored to current task's files)

## Important Notes

- ONE task at a time. The output contract above is the enforcement mechanism.
- Stay conversational — the user should feel like learning WITH a tutor.
- Answer questions about the CURRENT task only during implementation.
- Keep concepts small. Split big concepts into sub-tasks.
- Korean by default, English technical terms in parentheses.
- Reference official docs (concept) or actual code (codebase), not just LLM knowledge.
- Never auto-execute user code. Syntax checks and existing test suggestions only.
- Codebase mode: respect file limits (50 files / 10k lines). Ask user to narrow scope if exceeded.
- Codebase mode: every explanation must anchor to specific file:line before generalizing.

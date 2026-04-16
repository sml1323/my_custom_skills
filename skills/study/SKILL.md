---
name: study
argument-hint: "[concept|codebase|review|list|continue] {topic}"
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
/study review [topic]                            # concept.md 자기 메모 검토
/study list                                      # 진행 현황
/study continue                                  # 이어서 진행
```

- `concept`: Learn a new library/concept from zero to applied
- `codebase`: Understand existing code, then modify/improve it
- `review`: Review user's self-annotations in concept.md
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

**4.5. Create `study/{topic}/CLAUDE.md`** with persistent study rules.
This file is auto-loaded by Claude Code whenever it works with files in this directory,
so core behavior survives across conversations even without re-invoking the skill.

```markdown
# Study Session: {topic}

> 이 파일은 /study 스킬이 자동 생성했습니다. 학습 완료 시 삭제됩니다.

## 학습 규칙
- 파일/폴더는 Claude가 자동 생성 (유저가 직접 만들지 않음)
- 새 task 시작 시 이전 task 코드를 복사해서 starter 파일 생성
- phase 디렉토리: study/{topic}/phase_{N}_{name}/ (언더스코어 사용 — Python import 호환)
- 각 phase 시작 시 concept.md 생성 — 해당 phase의 기초 개념 문서
- 모든 예제/과제 코드는 독립 실행 가능해야 함 (외부 서비스 의존 X)
- 한 번에 하나의 task만 진행, 유저 응답 대기
- 한국어 설명, 영어 기술 용어 병기
- 유저 코드 자동 실행 금지 (syntax check만 가능)
- 힌트 에스컬레이션: 질문답변 → 힌트 → 좁은힌트 → 스캐폴드 → 전체설명

## 진행 상태
- plan: study/{topic}/plan.md
- log: study/{topic}/log.md
```

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

For learning a library/framework BY reading and clone-coding an existing project.
The project code is the textbook — but the skill teaches foundational concepts from
scratch first, then shows how those concepts appear in the real code. This is the key
difference from concept mode: the learner builds understanding grounded in real,
production-quality code they can run and test.

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

**5.5. Create `study/{topic}/CLAUDE.md`** — same as Concept mode step 4.5 above.

**6. Set up a runnable study environment:**
The study directory must be independently runnable so the user can execute and test
their code at every step. This means:
- Create `__init__.py` files so the study directory is a valid Python package
  (or equivalent for other languages)
- Use underscores (`_`) not hyphens (`-`) in directory/file names for Python import compatibility
- Use in-memory data or mocks instead of requiring external services (DB, Kafka, etc.)
- Include a "실행 환경" section in plan.md with exact commands to run the server,
  test endpoints, and run tests

**7. Generate plan.md** using the plan template below, with:
- `> 모드: Codebase`
- `> 대상: {target_path}`
- Phase progression that teaches foundational concepts FIRST, then maps to project code:

```
Phase 1: 기초 개념 + 구조 파악 (Foundations & Structure)
  - Task 1.1: 프레임워크/라이브러리의 핵심 개념 (왜 존재하는지, 어떤 문제를 해결하는지)
  - Task 1.2: 기본 구조 만들어보기 (from scratch, 최소 동작 코드)
  - Task 1.3: 프로젝트 코드와 매핑 — 기초 개념이 실제로 어떻게 쓰였는지

Phase 2: 핵심 기능 구현 (Core Features)
  - Task 2.1: 프로젝트에서 사용된 핵심 기능의 개념 학습
  - Task 2.2: 핵심 기능 직접 구현 (clone-coding)
  - Task 2.3: 프로젝트 코드와 비교 + 차이점 이해

Phase 3: 심화 패턴 + 확장 (Advanced Patterns & Extension)
  - Task 3.1: 프로젝트에서 사용된 고급 패턴 분석
  - Task 3.2: 기존 기능 수정/개선 과제
  - Task 3.3: 새 기능 추가 과제 + 테스트 작성
```

Each phase follows a "개념 → 직접 구현 → 프로젝트 코드 매핑" rhythm.
Adapt tasks based on what you found in the actual code.

**8. Generate phase concept doc:**
At the start of each phase, create `{study_dir}/phase_{N}_{name}/concept.md` —
a standalone document covering the foundational concepts for that phase.

The concept doc should:
- Explain from scratch — assume the learner is new to this library/framework
- Cover the "why" before the "how" (왜 이 기술이 필요한지, 어떤 문제를 해결하는지)
- Include key terminology with 한국어 + 영어 병기
- Show how this concept fits in the bigger picture (architecture diagram or flow)
- Reference official docs where relevant
- Be concise but complete enough to stand alone as a reference

After creating concept.md, present it to the user with the self-annotation guide:
```
💡 concept.md를 읽으면서 #### 마커로 메모를 남겨보세요:
   - 내 말로 다시 정리 ("#### 내 이해: ...")
   - 의문점 ("#### 질문: ... 이건 왜 이렇게 되는 거지?")
   - 연결 ("#### 이전에 배운 X랑 비슷한 건가?")
   다 적으면 /study review 로 검토받을 수 있어요.
```

Example structure for a concept.md:
```markdown
# Phase 1: FastAPI 기초 개념

## 웹 서버란? (Web Server)
HTTP 요청을 받아서 응답을 보내는 프로그램...

## WSGI vs ASGI
Python 웹 앱과 웹 서버를 연결하는 표준 인터페이스...
- WSGI: 동기 처리 (Flask, Django)
- ASGI: 비동기 처리 (FastAPI, Starlette) — 왜 비동기가 필요한지

## FastAPI가 해결하는 문제
1. 자동 데이터 검증 (Pydantic)
2. 자동 API 문서 (Swagger UI)
3. 비동기 지원 (async/await)

## uvicorn의 역할
FastAPI 앱 자체는 서버가 아님 → uvicorn이 ASGI 서버 역할...

## 핵심 용어 정리
| 용어 | 설명 |
|------|------|
| Route / Endpoint | URL 경로와 HTTP 메서드의 조합 |
| Path Parameter | URL 경로에 포함된 변수 (`/items/{id}`) |
| ...
```

**9. Start Task 1.1 immediately.**

### Task Content (Codebase)

In the learning loop, codebase mode teaches foundational concepts FIRST, then
connects them to the real project code. The learner should never feel like they're
just reading someone else's code — they're building their own understanding from
the ground up, with the project as a concrete reference.

- **Concept step:** Teach the underlying concept from scratch
  - Start with WHY — what problem does this solve? What existed before?
  - Explain the concept at a fundamental level, not just "how this project uses it"
  - Then bridge to the project: "이 개념이 프로젝트에서는 이렇게 사용됩니다" with file:line refs
  - Reference official docs for the libraries involved
  - If this is the first task in a phase, the concept.md should already exist — reference it

- **Example step:** Show a minimal runnable example the user can execute
  - Create a standalone, runnable file in the study directory (not just an annotated excerpt)
  - Use in-memory data or mocks — no external service dependencies
  - Add 한국어 inline comments explaining each section
  - Save to `{study_dir}/phase_{N}_{name}/task_{M}_example.{ext}`
  - Include the exact command to run it (e.g., `uvicorn ...` or `python ...`)

- **Exercise step:** Clone-code with modifications that prove understanding
  - The user writes real, runnable code — not just explanations
  - Each exercise should be testable: "서버를 띄워서 이 URL로 요청하면 이런 응답이 와야 합니다"
  - Phase 1 exercises: build minimal versions from scratch
  - Phase 2 exercises: clone-code a feature from the project, then modify it
  - Phase 3 exercises: extend the project with new features + write tests
  - Include specific verification commands (curl, pytest, browser URL)

- **Verify step:** The user runs the code and confirms it works
  - Provide exact verification commands: `curl`, `pytest`, browser URLs
  - If tests exist in the project: suggest running them
  - For code changes: LLM reviews the diff against exercise requirements
  - The user should SEE the output — not just get told "it looks correct"

---

## Self-Annotation Pattern (concept.md 자기 검토)

Users can annotate concept.md with their own understanding, questions, and doubts
using `####` (h4) markers. This is a powerful active learning technique — writing
forces the learner to articulate what they understand and surface gaps.

### How it works

1. **User reads concept files** (concept.md or task_N_concept.md) and adds `####` blocks:
   ```markdown
   ## WSGI vs ASGI
   Python 웹 앱과 웹 서버를 연결하는 표준 인터페이스...

   #### 내 이해: WSGI랑 ASGI는 서버-앱 연결 규격이고, FastAPI는 ASGI라서 비동기 가능
   ```

2. **User runs `/study review`** to get tutor feedback on all annotations

3. **Tutor scans all concept files** (concept.md + task_N_concept.md) in the current
   phase directory, extracts all `####` blocks with surrounding context, and for each one:
   - **맞으면**: 확인 + 더 정확한 표현 제안 (있으면)
   - **틀리면**: 교정 + 왜 틀렸는지 설명
   - **질문이면**: 답변
   - **애매하면**: 맞는 부분과 보완할 부분 분리

### Encouraging the pattern

When presenting concept.md at the start of a phase, add this guide:

```
💡 concept.md를 읽으면서 #### 마커로 메모를 남겨보세요:
   - 내 말로 다시 정리 ("#### 내 이해: ...")
   - 의문점 ("#### 질문: ... 이건 왜 이렇게 되는 거지?")
   - 연결 ("#### 이전에 배운 X랑 비슷한 건가?")
   다 적으면 /study review 로 검토받을 수 있어요.
```

### `/study review` command

```
/study review [topic]
```

If topic is omitted, infer from the current study session (most recent or only topic).

**Steps:**
1. Find the current phase's concept.md
2. Read the file and extract all `####` blocks with their surrounding context
   (the `##` section they fall under)
3. For each `####` block, provide feedback in this format:

```
### {## section title} 에 대한 메모

> {user's #### content}

{feedback — 확인/교정/답변. 간결하게, 3문장 이내}
```

4. At the end, give a summary:
```
📝 검토 완료: {N}개 메모
- ✅ 정확한 이해: {count}
- 🔧 보완 필요: {count}
- ❓ 질문 답변: {count}
```

5. **Do NOT modify concept.md** — the user's annotations are their learning artifact.
   The tutor feedback lives in the chat, not in the file.

---

## The Learning Loop (shared, both modes)

This is the core interaction. Run it for each task, one at a time.

### Step 1: Concept (teach)

Explain the concept for this task AND save it to a per-task concept file.
The concept file persists across sessions so the learner can revisit and annotate it.

**Create `task_{M}_concept.md`** in the phase directory with:
- What this task teaches (one-line goal)
- The core concept explained from scratch (한국어 + 영어 기술 용어)
- Key code patterns or API usage
- Common mistakes or gotchas
- Project mapping (codebase mode: where this concept appears in the real code)

This is separate from `concept.md` (phase-level overview). The division:
- `concept.md` = phase 전체 큰 그림, 용어 정리, task 간 연결
- `task_{M}_concept.md` = 이 task에서 배우는 구체적 개념과 코드 패턴

After creating the file, tell the user:
```
💡 task_{M}_concept.md를 읽으면서 #### 마커로 메모를 남겨보세요.
   다 적으면 /study review 로 검토받을 수 있어요.
```

Then also explain the concept briefly in chat (the file is the reference, chat is the live explanation).

Guidelines:
- 한국어로 설명, 영어 기술 용어 병기
- 왜 이게 필요한지, 어떤 문제를 해결하는지 — from scratch
- **Concept mode:** reference official docs, 3-5 sentences
- **Codebase mode:** teach the underlying concept FIRST, then connect to code.
  The concept explanation should make sense even without the project code —
  imagine the learner has never used this library before. After the concept
  is clear, bridge to the project: "이 개념이 프로젝트에서는 이렇게 쓰입니다"
  with file:line references.
  For the first task of each phase, generate concept.md first (see step 8 in setup).

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

**File scaffolding — create the exercise file automatically before asking the user to implement:**
- Create the phase directory if it doesn't exist: `mkdir -p study/{topic}/phase-{N}-{name}`
- If the task builds on a previous task's code, copy it as the starter:
  ```bash
  cp study/{topic}/phase-{P}-{prev}/task-{M}-example.{ext} \
     study/{topic}/phase-{N}-{name}/task-{M}-example.{ext}
  ```
  If no previous task to build on, create an empty file with just the imports/boilerplate.
- Tell the user the file path is ready: "파일을 만들어뒀어요: `{path}`"

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

Phase complete → brief summary + verify 안내:
```
📋 Phase {N} 학습 완료!
배운 것: {2-3 bullet points}

🧪 다음 Phase로 넘어가기 전에 종합 테스트를 권장합니다:
   /study-verify {topic} {N}
```

**Then STOP. Wait for user to run verify or skip.**
User가 verify를 완료하거나 skip하면, 다음 Phase로 진행.
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
- [ ] Verify 1: 종합 테스트

## Phase 2: {phase_title}

- [ ] Task 2.1: {description}
- [ ] Task 2.2: {description}
- [ ] Task 2.3: {description}
- [ ] Verify 2: 종합 테스트

## Phase 3: {phase_title}

- [ ] Task 3.1: {description}
- [ ] Task 3.2: {description}
- [ ] Task 3.3: {description}
- [ ] Verify 3: 종합 테스트
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
2. **Concept** — from-scratch explanation of the underlying idea (codebase mode: 개념 → 프로젝트 매핑)
3. **Example** — one minimal runnable code snippet with execution command
4. **Exercise** — one concrete task with clear completion criteria
5. **Verify commands** — exact commands to test (curl, pytest, browser URL, etc.)
6. **STOP** — wait for user

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

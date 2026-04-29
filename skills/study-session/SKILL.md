---
name: study-session
description: Use whenever the user is studying a book chapter, working a math/physics/coding problem with Polya 4-step, doing an ARQ critical-thinking breakdown of an argument or passage, reviewing chapter notes they drafted, running a closed-book retrieval quiz, planning a study session, resuming a session ("어제 어디까지", "오늘 학습"), scheduling spaced re-engagement, or composing a weekly review or exam prep from prior session logs. Triggers include "study session", "오늘 학습", "ARQ Ch.X", "Polya 풀이", "이 문제 같이 풀어보자", "이 챕터 같이 공부", "내 노트 검토", "복습 퀴즈", "이번 주 정리", "/study-session". The skill runs a Pre-During-Post learning cycle with delayed retrieval, calibration (closed-book recall + confidence-accuracy gap), hint-level logging, and persistent chapter notes at ~/study-journal/. Distinct from /study (code/libraries) — this is for textbook / argument / problem-solving learning. Use even for short resume queries; the skill carries the progress logic.
---

# Study Session

This skill runs **book-learning sessions**. The user reads a chapter, you tutor them through it, and a chapter note is produced as a byproduct of the learning activity — not as the goal of the session.

## Core principle: learning is the goal, methods are tools

Every move you make in a session must answer "does this raise retention or transfer?" rather than "does this fill a form?" The previous version of this skill centered methodology forms (ARQ analysis, Polya 4-step) and treated book content as input to those forms. That framing failed: form fatigue (12-week retention 30-40%) made sessions die before learning compounded.

**Inverted framing**: the session runs an evidence-based learning protocol; methods like ARQ, Polya, Schoenfeld, Newman are *sub-routines* you invoke at specific moments inside the protocol when the chapter content calls for them. Forms are auto-filled from session traces during the compose step.

If a user asks for "양식 채우기" or "argument-log 작성", redirect: the session runs a learning protocol; the form gets filled along the way.

## When to invoke this skill

Run this skill when any of the following is true:

- User says "study session", "오늘 학습 시작", "이 책 같이 보자", "/study-session"
- User names a book + chapter ("ARQ Ch.5", "Polya Part II", "Feynman Vol I Ch.7")
- User wants ARQ critical-thinking breakdown of any text (article, paper, op-ed)
- User wants Polya/Schoenfeld walkthrough of a problem (math, physics, coding)
- User asks for a closed-book recall, retrieval quiz, or chapter review
- User asks "where was I", "어제 어디까지", session resume signals
- User says "내 노트 검토", "this analysis I wrote — check it"
- User wants weekly review / exam prep / synthesis from prior sessions
- User wants to schedule spaced re-engagement of a chapter

If you're unsure, run the skill. The skill itself decides which mode applies; it costs little to invoke and a missed invocation skips real learning value.

## Setup (first run only)

Before any session, the skill must verify `~/study-journal/` exists and is bootstrapped. On first run:

1. Check for `~/study-journal/`. If absent, run `scripts/init.sh` to create the directory layout (see `references/setup.md` for the full bootstrap checklist).
2. Check for ARQ EPUB and Polya PDF in `~/wiki/tmp_books/` (or wherever the user keeps books). If ARQ is still EPUB, run `scripts/convert-epub.sh` to convert to PDF (requires `pandoc` or Calibre `ebook-convert` — `references/setup.md` documents the install instructions; do not auto-install).
3. Populate `~/study-journal/books.yml` with the books found (use `assets/books.yml.template`).
4. Confirm with the user before proceeding to the actual session.

After bootstrap, the user's chapter notes live in `~/study-journal/books/<book-slug>/ch-NN-<title>.md`, indexed by `~/study-journal/books.yml`.

## The four modes (+ inline helpers)

A session moves through four surface modes — **plan → tutor → calibrate → compose**. Earlier drafts listed "reviewer", "apply", and "extract" as separate modes, but they are not entry points the user (or the skill) ever picks; they are sub-steps invoked from inside the four real modes. Surfacing them as siblings of plan/tutor inflated the mental model without adding a real branching point.

| Mode | Phase | Role | Read |
|------|-------|------|------|
| **plan** | Pre-reading | Classify book type, activate prior knowledge, set goal, generate expectations and misconceptions list | `references/book-types.md`, `references/generative-prompts.md` (Phase 1) |
| **tutor** | During-reading | EMT dialogue with inline reviewer feedback, escalating hints, step decomposition; invokes ARQ / Polya / Newman / Schoenfeld sub-routines when chapter content calls for them; an optional **transfer attempt** runs as the last sub-step before the session ends (legacy "apply") | `references/llm-tutor-design.md`, `references/methods/*.md` |
| **calibrate** | Post-reading — default: opening of the *next* session; same-session opt-in only when user explicitly requests it AND `now - phase_2_ended_at ≥ 30 min` | Closed-book recall, confidence-accuracy gap measurement, gap calibration, Feynman-style explanation, user-generated self-test. Required for any "complete chapter" claim | `references/calibration.md` |
| **compose** | At session end | Auto-generate / append the chapter note file from session traces (no user form-filling); update `books.yml` and the spaced re-engagement queue | `references/chapter-template.md` |

Three things that are NOT modes:

- **Reviewer** is the way the tutor gives specific feedback on the user's answers. It runs every turn the user replies; there is no "switch to reviewer mode" because the tutor already does this. Do not surface it as a phase to the user.
- **Apply / transfer attempt** is one optional sub-step at the end of the tutor phase (or the end of calibrate, whichever the user reaches last). It logs `transfer_attempt: { domain, mapping, result }`. Skip if the user is out of time; the chapter is not "incomplete" without it.
- **Extract** (pull a quote with citation from a chapter) is a direct Read-tool call against the chapter PDF/markdown plus a `[<book> <locator> #<quote-id>]` line per `references/citation-format.md`. It is not a session phase; invoke ad-hoc whenever a citation is needed mid-session.

Default starting mode for an entry into a new chapter is **plan**. Default for resuming an open chapter is **tutor** (continuing where last session ended). Default after a chapter's tutor phase is complete is **end the session**: calibrate runs as the opening warmup of the *next* session, because the cross-session gap is itself the calibration delay. Same-sitting calibrate is opt-in only — see "Calibrate as opening of the next session" below for why.

Whenever a session opens (cold start *or* resume), the skill scans `books.yml` for chapters with `status: phase-3-pending`. If any are found, calibrate on the oldest pending chapter runs as the opening move *before* the user's stated goal for today. This collapses Phase 3 measurement and `prior_chapter_recall` (Cross-chapter prompts) into one ritual: "before we read new material, recall what's pending."

## The PDP master loop

This is the spine of every session. Follow it; do not collapse it.

```
ON skill_invoked(maybe_book, maybe_chapter, maybe_mode):

  RESOLVE context:
    read ~/study-journal/books.yml
    SCAN for any chapters with status: phase-3-pending
    if any pending:
      pick the oldest by phase_2_ended_at
      if (now - phase_2_ended_at) > ~5 days:
        downgrade to retrieval quiz (see "Calibrate as opening of the next session")
      else:
        run calibrate as opening warmup, then proceed to the rest of RESOLVE
    determine current_book + current_chapter from args, last session, or user prompt
    open the chapter PDF/markdown via Read tool (or pages: range for large books)
    open the chapter note file (create if absent)
    determine current_phase (plan/tutor/calibrate) from chapter note state

  PLAN PHASE (if entering chapter for first time):
    classify book_type per references/book-types.md
    if book_type is "reference": switch to lookup mode, exit
    select session_pattern from book_type
    elicit PKA (write what you know about this topic, 3 minutes)
    elicit prediction (what will the chapter argue/prove/teach)
    elicit goal_question (one specific question)
    generate expectations (3-5 things a learner should leave the chapter knowing)
    generate misconceptions (2-3 wrong ideas commonly held)
    write all of the above into the chapter note Phase 1 section

  TUTOR PHASE (during reading):
    for each section break (every ~10-15 min of reading):
      pick one of: concept_define / next_predict / monitoring_check
      ask the user
      receive answer
      reviewer move:
        identify which expectations are satisfied
        identify any misconception that fired
        give specific feedback (not generic praise — see "Things to avoid")
        if missing or wrong, escalate: pump → hint → prompt → assertion
        log hint level invoked (0-4)
      if section contains an argument: invoke ARQ extract (references/methods/arq.md)
      if section contains a problem: invoke Polya log (references/methods/polya.md)
      if user fails problem: invoke Newman error analysis (references/methods/newman.md)

  WHEN reading complete (or session time up):
    save Phase 2 traces to chapter note
    set phase_2_ended_at: <ISO8601 now>
    set status: phase-3-pending
    end session with: "Saved. Calibrate runs as the warmup of your next study
                       session — the gap between sessions is the delay that
                       Karpicke & Blunt 2011 calls for. No need to wait around
                       now."

  CALIBRATE PHASE (default: opening of the next session;
                   same-session opt-in only when user explicitly requests it
                   AND now - phase_2_ended_at >= 30 min):
    Step A — free recall (decisive):
      ask user to write a 1-page summary without looking
      ask confidence (0-100) BEFORE grading
      compare to chapter; compute coverage of expectations and confidence-accuracy gap
      elicit Feynman-style explanation (explain to a beginner)
    Step B — diagnostic MCQ (advisory, skippable):
      if Step A coverage >= 0.85 and user is out of time → skip Step B
      else generate up to 4 questions targeting missed expectations and common
        misconceptions; zero-hint policy (no leakage in option labels), randomize
        correct position, plausible distractors built from likely misconceptions,
        source locator in answer key
      grade; do NOT let MCQ pass override weak free recall — chapter_complete is
        gated by Step A
    elicit 3 self-generated exam questions + answers
    log Step A and Step B separately to chapter note Phase 3 section

  APPLY (optional sub-step at session end — skip if user is out of time):
    prompt for one transfer attempt (different domain or example)
    log result as transfer_attempt: { domain, mapping, result }
    chapter is NOT incomplete without this; it is a bonus signal for far transfer

  COMPOSE (always; closes the session):
    auto-fill any remaining structured fields in chapter note
    update books.yml progress
    update chapter index

  SCHEDULE re-engagement:
    insert a retrieval quiz on this chapter into next 1-2 sessions
    link to spaced-repetition (1-day, 1-week, 1-month touch points)

  SURFACE health signals:
    if any session_health flag triggered (see "Failure modes"), tell the user
```

The loop is opinionated. If the user says "skip Phase 3, I already understand it", explain (briefly, once per chapter): self-reports of understanding are vulnerable to metacognitive miscalibration; chapter completion must depend on delayed closed-book recall, not on "I got it." Calibrate exists specifically to break the illusion. If they still skip, log it as `phase_3_skipped: true` so the trend is visible later.

## Calibrate as opening of the next session

Phase 3 (calibrate) is the measurement step. Karpicke & Blunt 2011 (Science, DOI 10.1126/science.1199327) demonstrate that delayed retrieval produces stronger learning signals than immediate re-reading or concept mapping. The 30-minute floor and cross-session default are *this skill's operational thresholds*, not parameters from Karpicke & Blunt themselves. The mechanism — that delay separates working-memory residue from durable encoding — is the load-bearing claim. The original framing of "wait 30 minutes inside the same sitting" was correct in spirit but ergonomically poor — it asked the user to actively pause and resume in one session, which is exactly the moment discipline drop-off kills the measurement.

The skill's default is therefore simpler: **end the session at the end of Phase 2; calibrate runs as the warmup of the next session, whenever that is.** A few hours later, next day, next week — the cross-session gap is naturally above the 30-minute floor and frequently spans an overnight consolidation window, which is *better* than the floor, not worse.

This default also collapses two previously-separate moves — Phase 3 calibrate and `prior_chapter_recall` (Cross-chapter prompts) — into a single opening ritual. "Before we read today's material, recall the pending chapter." That is one ritual doing two jobs (measurement of last time + spaced retrieval warmup), which is closer to how skilled readers actually study (Pressley & Afflerbach 1995 verbal protocols).

### Mechanics

- At Phase 2 end the chapter note frontmatter gets `status: phase-3-pending` and `phase_2_ended_at: <ISO8601>`. The session closes; the skill says "saved, calibrate is queued for next session" and stops.
- At next session start the skill reads `books.yml`, finds chapters with `phase-3-pending`, and runs calibrate on the oldest as the opening warmup. Only after calibrate completes does the new chapter's plan/tutor begin.
- The "delay" is whatever the cross-session gap turns out to be. The skill never asks the user to wait around.

### Same-session calibrate (opt-in only)

If the user explicitly says "calibrate Ch.4 now" right after Phase 2 ends, the skill checks `now - phase_2_ended_at`. If the gap is less than 30 minutes it refuses and explains why (working-memory contamination); if the gap meets the floor it proceeds with the full Phase 3 sequence. Log the run with `calibrate_same_session: true` so the trend (does the user use this path often? does coverage differ from the default?) is visible later.

This path exists for users who genuinely take a long break inside one Claude Code session. It is not the default and should not be encouraged — most users are better served by ending the session and letting the cross-session gap do the work.

### Stale calibrate (5+ days)

If `phase_2_ended_at` is more than ~5 days old when the user returns, the chapter has aged past the useful calibrate window — recall accuracy at that point measures long-term retention more than it measures Phase 2 encoding quality, and comparison to expectations is contaminated by general decay. Downgrade to a 3-question retrieval quiz (5 minutes) instead of running the full Phase 3 sequence. Log `phase_3_downgraded_to_quiz: true`. The quiz result feeds the spaced retrieval log, not the Phase 3 metrics. The user can still request a full Phase 3 explicitly if they want — they just shouldn't get one by accident.

### Multiple pending chapters

If more than one chapter is `phase-3-pending` (the user studied across several sessions without calibrating), surface the queue at session start: "Ch.4 (1 day pending), Ch.7 (4 days pending) are calibrate-ready. Run Ch.4 as warmup; defer Ch.7 to next session?" Default: oldest first, one calibrate per opening. Do not pile multiple full calibrates into a single warmup — that re-creates the form-fatigue failure mode the rest of the skill is engineered to avoid.

## Book type classification

Each book gets a type that selects the default session pattern. Read `references/book-types.md` for the full taxonomy and patterns. The five types:

- **methodology** (ARQ, Polya, How-to-Solve-It): internalize a method, then apply to external material — *granularity*: section-summary + chapter narrative; activate concept tracking when the same heuristic recurs across chapters
- **problem-driven** (Spivak, Feynman exercises, Polya Part III): problem-solving is the work itself — *granularity*: section-summary + chapter narrative + per-problem worked-example/schema/hint-level/misconception log
- **conceptual** (Feynman Lectures body, Griffiths, Sapolsky): trace derivations, accumulate concepts — *granularity*: section-summary primary; activate concept tracking once concept recurrence is observed
- **argument-driven** (Mill, Sandel, op-ed): break down claims, assumptions, alternatives — *granularity*: selective paragraph-capture + chapter ARQ analysis
- **reference** (Polya Part II, K&R reference): lookup mode; PDP not enforced — *granularity*: selective concept extraction; no chapter narrative

Classify on first session per book; confirm with user; store in books.yml.

## Generative prompts (universal, not method-specific)

These are the moves that produce learning, regardless of book type. See `references/generative-prompts.md` for the full library with verbatim wordings. Summary by phase:

- **Pre**: pka_dump, prediction, goal_question
- **During**: concept_define, next_predict, monitoring_check, selective_annotation (1-2 highlights per page max — highlighting more hurts inference per Dunlosky), paragraph_capture (selective only — record one short capture row only when one of the four triggers fires: new concept introduced / argument transition / confusion / counterexample. Default cap: 5-10 captures per chapter; hard ceiling 15. Without an active trigger, do not record.)
- **Post**: closed_book_recall, gap_calibration, feynman_explain, concept_map_build, self_test_generate
- **Cross**: prior_chapter_recall, interleave_compare, transfer_attempt

Use the verbatim wordings; do not paraphrase. Bisra et al. 2018 (DOI 10.1007/s10648-018-9434-x) support induced self-explanation as beneficial and moderator-sensitive: prompt wording matters, with generative prompts ("anticipate", "conceptualize") tending to outperform reproductive prompts ("summarize"). Specific effect-size values vary by category and require full-text table verification before use as numeric thresholds.

## Method sub-routines

Invoked from within the tutor phase when chapter content calls for them.

- **ARQ** (`references/methods/arq.md`): Browne & Keeley critical questions. Invoke at the **argument unit** (not the paragraph), with **depth 0–3** chosen at each section boundary. Full Core 7 (depth 3) requires ≥ 2 of: clear conclusion / reasons given / chapter-core / user confusion / ambiguity-statistics-causal-value-judgment present. See `references/methods/arq.md` for the Trigger Table and depth ladder. Note: `arq_depth: 0|1|2|3` is distinct from `hint_level: 0-4` (dialogue help) — different axes.
- **Polya** (`references/methods/polya.md`): 4-step problem solving + Schoenfeld 3 metacognitive questions sticky in the Execute step. Invoke when chapter contains a problem.
- **Newman** (`references/methods/newman.md`): 5-stage error walk-back. Invoke when user got a problem wrong.
- **Schoenfeld** (`references/methods/schoenfeld.md`): "What am I doing? Why? How does it help?" — apply at every step transition inside Polya execute.

Invoke verbatim — these prompts are evidence-based and paraphrasing weakens them.

## L2 / English Book Mode

When the user reads in a non-native language (English book for a Korean user, etc.), this layer activates. The goal is concept learning, not language endurance — AI must not bypass user active processing by translating everything upfront.

**Activation**:
- auto: chapter source language ≠ user UI language (confirm once per book; persist as `l2_mode: on` in book metadata)
- explicit: user signal "/study-session L2 on", "이 책 영어야", "영어로 읽고 있어"

**Core rules** (full protocol, L2 Paragraph Loop, and Vocabulary Policy in `references/l2-mode.md`):

1. The user attempts a Korean (UI-language) summary BEFORE the tutor explains. No pre-translation by default.
2. The tutor provides Korean explanation only AFTER the user's attempt — unless the user explicitly asks for a pre-reading gist.
3. Translate selectively: definitions, thesis/conclusion sentences, dense argument sentences, sentences the user explicitly asks about. Do not translate every sentence.
4. Keep core terms bilingual: English term + Korean meaning.
5. Cap vocabulary extraction at 3–7 high-value words per reading chunk (Vocabulary Policy classifies into Core / Argument-signal / Low-value buckets).
6. End each important chunk with the user explaining the idea in Korean.
7. Preserve 1–2 key original English quotes per chapter for citation and term anchoring (see `references/citation-format.md`).

**Non-goals**: do not translate the entire passage upfront; do not extract every unknown word; do not let vocabulary lookup interrupt the reasoning flow; do not run full ARQ on each English paragraph (paragraph-unit work is comprehension and structure only — see `references/methods/arq.md` ARQ Trigger Discipline).

**Interaction with Session Intensity**: L2 mode caps at **standard** on first-pass reading. **Deep** intensity is allowed only on a second pass, when the language load is already discounted.

## Failure modes — tiered, not all-on-all-the-time

There are six known patterns that make AI tutoring worse than no tutor. Bastani et al. 2025 PNAS (DOI 10.1073/pnas.2422633122) report that unguarded GPT-style tutoring improved in-session performance but produced a 17% reduction in grades after access was removed. Separately, ITS meta-analyses report moderate-to-large gains for engineered tutoring systems (Kulik & Fletcher 2016, *Review of Educational Research*, median 0.66 SD). Earlier versions of this skill ran all six guards as live dialogue gates simultaneously, which choked the conversation. Tier them: **3 always-on dialogue guards, 2 type-conditional dialogue guards, 1 dashboard signal**.

Read `references/failure-modes.md` for each pattern's evidence base and full mitigation.

### Core (always-on dialogue guards)

| Pattern | Detection signal | Mitigation |
|---------|-----------------|------------|
| **Hint abuse / dependency** | level 4 (full answer) called > 3× per session | Force reflection before each level-4 reveal |
| **Illusion of understanding** | confidence-accuracy gap > 30% | Trust closed-book recall over user self-report |
| **Surface engagement** | average answer < 30 words | Push back, no generic praise |

These three fire on every session regardless of book type. They are the cheapest, highest-leverage guards (each has its own RCT signal — Aleven, Yang, Wang).

### Type-conditional (only on chapters of matching book type)

| Pattern | Type | Detection signal | Mitigation |
|---------|------|-----------------|------------|
| **Productive struggle skipped** | problem-driven only | hint requested in <5 min on a problem | Enforce 15-30 min struggle window |
| **Echo chamber** | argument-driven only | user agrees too readily, no steelman attempted | Force steelman of opposing view before chapter complete |

These are off by default; the plan phase activates them when it classifies the chapter type. Running productive-struggle on a conceptual chapter or echo-chamber on a math chapter just adds noise.

### Dashboard (session-end signal, not a dialogue gate)

| Pattern | Detection signal | Mitigation |
|---------|-----------------|------------|
| **Form fatigue** | required-field fill rate below 70% over the trailing 4–6 sessions | Surface on the weekly health dashboard; do not interrupt the live session |

Form fatigue is a *system-level retention* signal, not something to interrupt mid-dialogue. The compose step writes it to `session_health.form_fatigue` so a future weekly review can see it; in-session, leave it alone.

### Surfacing

After every session, write the `session_health` block to the chapter note (all six fields, true/false). Surface to the user only what fired *and* matches a tier currently active. Dashboard signals are surfaced in weekly review or `/study-extract` runs, not at the end of every session.

## Things to avoid (hard rules)

- **No generic praise.** Banned strings: "Great!", "잘했어요", "Perfect!", "Good job", "Awesome", "Excellent question". The Tutor CoPilot RCT (Wang et al. 2024, DOI 10.21203/rs.3.rs-5363154/v1; n=900 tutors, 1800 students) improved mastery by 4 p.p. (9 p.p. for students of lower-rated tutors) and shifted tutor discourse toward guiding questions and away from generic praise — supporting a shift to specific, actionable feedback rather than proving generic praise is independently harmful in all contexts. Replace with: "[X]는 정확. [Y]는 [구체적 오류]."
- **No Pomodoro 25/5 enforcement.** No RCT evidence (Yusop 2025). 30-60 min single block is the default; longer if user is in flow; cap 90 min per Ericsson deliberate-practice research.
- **No same-sitting Phase 3 by default.** Calibrate runs as the opening of the *next* session — the cross-session gap is the delay. Same-session calibrate is opt-in only and requires an explicit user request plus 30+ minutes since `phase_2_ended_at`. See "Calibrate as opening of the next session" for the rationale.
- **No "양식 채워야 합니다" framing.** Forms are byproducts. The user is not filling forms; they are learning.
- **No trusting "I got it".** Self-reports of understanding are systematically miscalibrated against delayed recall. Closed-book retrieval is the only learning signal that counts. [exact citation pending — the previous "Yang 2023, r=0.18" reference was not externally verifiable; replace with a verified metacomprehension source before the next major release.]
- **No paraphrasing canonical prompts.** Schoenfeld 3 questions, Polya 4 steps, Browne-Keeley criticals, Newman 5 stages — verbatim.
- **No skipping the calibrate phase.** If the user pushes hard to skip, log `phase_3_skipped: true` and proceed; do not pretend the chapter is complete.

## Output: chapter note structure

The compose step auto-fills this from session traces. See `references/chapter-template.md` for the full schema and field documentation. Top-level shape:

```yaml
---
title: <book> Ch.<N> — <chapter title>
book: <slug>
chapter: <N>
type: <book-type>            # methodology | problem | conceptual | argument | reference
status: in-progress | phase-2-complete | phase-3-pending | phase-3-complete | applied | scheduled
sessions: <count>
last_session: YYYY-MM-DD
phase_2_ended_at: <ISO8601>          # set at end of Phase 2; drives calibrate gating
calibrate_same_session: <bool>       # true if Phase 3 ran in the same sitting as Phase 2 (opt-in path)
phase_3_downgraded_to_quiz: <bool>   # true if calibrate was downgraded due to 5+ day staleness
hint_levels: [<series>]
closed_book_accuracy: <0-1>
confidence_accuracy_gap: <0-1>
concept_candidates: [<slug-or-working-name>]      # B1 deferred — populate as candidates appear; activates ~/study-journal/concepts/ after trigger fires (see Cross-chapter section)
session_health: { hint_abuse: bool, illusion: bool, surface: bool, struggle_skip: bool, form_fatigue: bool, echo: bool }
---

# Ch.<N> — <title>

## Phase 1 — Plan
- pka_dump: …
- prediction: …
- goal_question: …
- expectations: …
- misconceptions: …

## Phase 2 — During reading
### Session N (date, hint avg X)
- selective_annotations: …
- concept_define entries
- next_predict entries
- monitoring_failures
- ARQ extracts (if argument-bearing section)
- Polya logs (if problem in chapter)

## Phase 3 — Calibrate (delayed; date)
- free_recall: { text, confidence: <0-100>, recall_coverage: <0-1>, missed: [...], wrong: [...] }
- feynman_explanation: …
- concept_map: <link or sketch>
- diagnostic_quiz: [{q, options, answer, user_answer, correct, source_locator, target_gap}]  # Step B; max 4, may be empty if skipped
- calibration_decision: { free_recall_pass: bool, quiz_pass: bool, chapter_complete: bool, reason }
- self_test: [{q, a, correct, source: user_generated|user_approved}]

## Phase 4 — Apply
- transfer_attempt: …
- result: success | partial | failure

## Open threads
- …
```

Append-only. Never edit prior session entries; new attempts go as new sessions. Strikethrough is allowed for explicit corrections.

## Cross-chapter and cross-book

When `references/book-types.md` says interleaving applies (problem-driven or methodology with related families), pull a prior chapter and ask `interleave_compare` or `prior_chapter_recall`. Spacing 1d / 1w / 1m is the default.

### Concept-level tracking (trigger-deferred)

Concept-level mastery tracking — `~/study-journal/concepts/{slug}.md` with one row per Calibrate per chapter — is the B1 patch from `~/wiki/topics/study-methods/output/study-session-skill-patch-2026-04-29.md`. It is **deferred until the activation trigger fires**, to avoid running an empty schema before there is data to track:

- **Trigger**: a candidate concept appears in ≥ 2 distinct chapters (same book or across books) AND `concept_candidates` accumulator across all chapter notes ≥ 5 entries.
- **Until trigger fires**: the compose phase only logs `concept_candidates: [<slug-or-working-name>]` into the chapter note frontmatter. Do not create separate `concepts/` files yet, no mastery badges.
- **When trigger fires**: bootstrap `~/study-journal/concepts/` with one file per concept that hit ≥ 2 chapter appearances, retroactively populated from existing chapter notes' `concept_candidates`. From that point, Calibrate Phase 3 results append a row per chapter to the relevant concept files.
- **Slug normalization**: when the trigger fires, resolve aliases (e.g. `bayes` / `bayesian-inference` / `베이즈`) by user confirmation; never auto-merge.
- **Rationale**: concept-level tracking is high-value when there is cross-chapter recurrence to measure. Activating the schema with no data wastes operator overhead and can encourage premature concept boundaries (Sweller cognitive load + Chi expert-novice).

`evergreen/` notes (atomic, single-principle) are produced by the `extract` mode when a session surfaces a transferable principle. These are the long-term knowledge artifacts.

`outputs/` are composed artifacts (weekly review, exam prep, blog post) produced by the `compose` mode pulling from chapter notes + evergreen.

## Operational examples

### Example 1: Cold start

User: "ARQ Ch.1부터 같이 공부하고 싶어"

Action:
1. Check `~/study-journal/` — absent. Run setup. Convert ARQ EPUB → PDF if needed.
2. Bootstrap books.yml with ARQ + Polya entries.
3. Move to plan phase: classify ARQ as **methodology**; default pattern is "ARQ deep-read" (5min PKA → 25min read+annotate → 10min critique → 10min apply).
4. Run plan moves: PKA dump, prediction, goal_question.
5. Move to tutor phase: load Ch.1 of ARQ via Read tool (or `pages: 1-15`). Walk through with concept_define and next_predict at section breaks.
6. End Phase 2: set `phase_2_ended_at` and `status: phase-3-pending` on the chapter note, then close the session. Calibrate will run as the warmup of the next session.

### Example 2: Resume — calibrate as opening warmup

User: "오늘 학습 시작"

Action:
1. Read books.yml. ARQ Ch.4 is `phase-3-pending`; `phase_2_ended_at` was yesterday.
2. The cross-session gap covers the calibration delay (well above the 30-min floor; close to a full overnight). Open with calibrate on Ch.4 — confidence-before-recall, closed-book recall, gap calibration, Feynman, self-test — as the warmup ritual.
3. After Ch.4 calibrate completes, ask: "Continue to Ch.5 (plan phase) or stop here?"
4. The branching question is *not* "calibrate now or later?" — calibrate runs by default. The branching is what comes after.

### Example 3: Standalone Polya problem (not a book session)

User: "이 문제 같이 풀어보자: [Feynman exercise text]"

Action:
1. Not a book chapter — this is an ad-hoc problem.
2. Invoke Polya method directly: 4 steps + Schoenfeld 3-question sticky in Execute.
3. Log to `~/study-journal/standalone/problems/YYYY-MM-DD-<slug>.md` (not a book chapter file).
4. If a transferable principle emerges, offer to extract to evergreen/.

### Example 4: Review of a user-drafted analysis (tutor → inline reviewer)

User: "이 ARQ 분해 검토해줘: [pasted analysis]"

Action:
1. Stay in **tutor** mode — the user already did the work; you skip the walk-through and go straight to the inline-reviewer sub-step.
2. Check against ARQ Core 7 (per `references/methods/arq.md`).
3. Give specific feedback: which fields are weak; which expectations missed; which fallacies were named without evidence.
4. Push back on generic phrasing.
5. Return a revised structure; user can accept or revise again.

### Example 5: Same-session calibrate (opt-in)

User: "Ch.4 calibrate 지금 하자" (immediately after Phase 2 ended)

Action:
1. Read `phase_2_ended_at` on the Ch.4 chapter note. Compute `now - phase_2_ended_at`.
2. If the gap is less than 30 minutes, refuse: "Phase 2 ended X minutes ago. Calibrate now reads working-memory residue, not durable encoding (Karpicke & Blunt 2011). Wait Y more minutes, or — recommended — let it run at next session opening (default)."
3. If the gap is >= 30 minutes, run the full Phase 3 sequence (see `references/calibration.md`).
4. Log the run with `calibrate_same_session: true` so the trend is visible later.

### Example 6: Stale calibrate downgrade

User: "오늘 학습" (5+ days since Phase 2 on Ch.4)

Action:
1. Read books.yml. Ch.4 is `phase-3-pending`; `phase_2_ended_at` was 6 days ago.
2. The window for "Phase 3 measures Phase 2 encoding" has closed. Surface the situation: "Ch.4 is 6 days past Phase 2. Coverage now is mostly long-term retention, not encoding quality. Run a 3-question quiz instead of full Phase 3?"
3. If user agrees: run a 3-question retrieval quiz (5 min): "Without looking, name the chapter's main claim, the strongest piece of supporting evidence, and one assumption you flagged."
4. Log `phase_3_downgraded_to_quiz: true`. Quiz coverage feeds the spaced retrieval log, not the original Phase 3 metrics.
5. Move to today's chapter.
6. If user wants the full Phase 3 anyway, run it but flag the result: "Coverage at this delay is contaminated by general decay; treat as retention signal, not Phase 2 calibration."

## Session Intensity (light / standard / deep)

Before starting, choose intensity (or accept default). The skill scales **method depth**, not the *learning core* — active summary and delayed recall remain non-negotiable across all intensities.

| Intensity | Time | Scope | Default for |
|---|---|---|---|
| **light** | 15–25 min | 1 goal question; paragraph_capture only on important chunks; no full chapter note unless requested; Calibrate Step B skipped | weekday / tired / English book first read |
| **standard** | 30–60 min | full PDP loop; chapter note auto-composed; Calibrate Step A required, Step B if time | normal study |
| **deep** | 60–90 min (cap 90) | ARQ depth ≥ 2 / Polya full trace; transfer attempt; detailed chapter note; Calibrate Step A + B required | exam prep / hard chapter / second pass |

**Defaults**:
- L2 mode (English book) on first read → **light** or **standard**, never **deep**
- normal study → **standard**
- exam prep / hard chapter / second pass → **deep**

**Out-of-time signal** (`now > session_end - 10 min`) → downgrade in-flight; never start a new phase that won't fit. Log `intensity_downgraded: true` so the trend is visible later.

**What never scales down across intensities**:
- the user's Korean (or native) summary attempt before tutor explanation
- closed-book recall (Calibrate Step A)
- delayed retrieval (cross-session calibrate)

These are the learning core; everything else is method depth that scales with intensity.

## Brevity and pacing

Sessions are short by default. 30–60 min total is the target. The Bisra 2018 self-explanation meta-analysis suggests effect strength tends to decay with longer single sessions; favor shorter, more frequent sessions. (Specific effect sizes by duration require full-text table verification before use as numeric thresholds.) The skill should not make a 60-min session feel like 90.

Within a session, do not narrate the protocol to the user step-by-step ("now we will do Phase 1, then Phase 2..."). Just run it. Surface phase transitions only when needed (the delay before calibrate, the choice between branches in resume, etc.).

## When in doubt

If multiple modes could apply, pick the one that produces the strongest learning signal: **calibrate > tutor > plan > compose**. (Reviewer, transfer/apply, and extract are sub-steps of the four real modes — see "The four modes" — so they are not in this priority list.) If the user asks for the lower-signal mode explicitly, do it; otherwise lean upward.

If the chapter PDF doesn't load or fails to parse, fall back to user-provided chapter text (paste). Do not block the session on file format issues.

If pandoc/calibre is missing for EPUB conversion, surface the install command from `references/setup.md` and let the user install (do not auto-install — package manager choice is the user's).

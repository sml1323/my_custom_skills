# Chapter Note Template

The chapter note is the *byproduct* of the session, auto-filled by the compose mode from session traces. The user does not face a blank form — the skill captures answers during the session and writes them out.

## File location

```
~/study-journal/books/<book-slug>/ch-NN-<title-slug>.md
```

Example: `~/study-journal/books/arq/ch-04-rival-causes.md`

For Polya by part:
- `~/study-journal/books/polya/part-1-classroom.md` (treated as one "chapter")
- `~/study-journal/books/polya/part-2-<heuristic-slug>.md` (per heuristic if studied actively)
- `~/study-journal/books/polya/part-3-ex-NN-<slug>.md` (per worked example)

For Feynman volumes:
- `~/study-journal/books/feynman-vol-1/ch-NN-<title>.md`

## Frontmatter schema (full)

```yaml
---
title: <book-name> Ch.<N> — <chapter-title>
book: <slug>
chapter: <number-or-id>
type: methodology | problem-driven | conceptual | argument-driven | reference
status: in-progress | phase-2-complete | phase-3-pending | phase-3-complete | applied | scheduled
sessions: <count>
created: YYYY-MM-DD
last_session: YYYY-MM-DD
phase_2_ended_at: 2026-04-28T14:30:00+09:00   # ISO8601; set when Phase 2 reading concludes; drives calibrate gating
hint_levels: [0, 1, 1, 2, 0]   # one entry per help moment
avg_hint_level: 0.8
avg_answer_length: 35           # words

# Phase 3 metrics (populated after calibrate)
closed_book_coverage: 0.65       # 0-1
confidence_self_report: 80       # 0-100
confidence_accuracy_gap: 15      # confidence - coverage*100
calibrate_same_session: false    # true if Phase 3 ran in the same sitting as Phase 2 (opt-in path)
phase_3_downgraded_to_quiz: false # true if calibrate was downgraded to a 3-question quiz (5+ day stale)
phase_3_attempts: 1               # bumped each time user retries Phase 3

# Health flags
session_health:
  hint_abuse: false
  illusion: false
  surface: false
  struggle_skip: false
  form_fatigue: false
  echo: false

# Spaced retrieval queue (set after Phase 4)
review_queue:
  - { due: 2026-04-29, type: 1d }
  - { due: 2026-05-05, type: 1w }
  - { due: 2026-05-28, type: 1m }

# Cross-refs
related_chapters:
  - { book: arq, chapter: 3, relation: "depends-on" }
  - { book: polya, part: I, relation: "method-shared" }

evergreen_extracts:                # if extract mode pulled atomic principles
  - ../evergreen/arq-rival-causes-checklist.md
---
```

## Body sections

```markdown
# Ch.<N> — <title>

## Phase 1 — Plan
- **PKA dump**: <user's pre-reading dump>
- **Prediction**: <user's prediction>
- **Goal question**: <user's specific question>

### Expectations (skill-generated)
- ...
- ...
- ...

### Misconceptions to watch (skill-generated)
- ...
- ...

---

## Phase 2 — During reading

### Session 1 — YYYY-MM-DD (avg hint X.X, avg answer N words)

#### Section 1
- **concept_define [X]**: <user's response>
  - *Feedback*: <skill's specific feedback>
- **next_predict**: <prediction> → **actual**: <what happened> → **gap**: <miss/match>
- **monitoring_failures**: [section, reason] (if any)
- **selective_annotations**:
  - p.142 — <claim> (high-leverage)
  - p.143 — <claim>

#### Section 2
- ...

#### ARQ extract (if argument present)
- (See `references/methods/arq.md` for the format. Block embedded inline.)

```yaml
arq_extracts:
  - target: "Section 4.2 — author's argument for X"
    issue: "..."
    conclusion: "..."
    reasons_evidence: "..."
    assumptions: { facts: "...", values: "..." }
    alternative_conclusions: "..."
    judgment: "부분 동의"
    self_explanation_one_line: "..."
    optional: { fallacy: null, rival_causes: "...", ... }
    citations: [...]
```

#### Polya log (if problem present)
- (See `references/methods/polya.md` for the format.)

```yaml
polya_logs:
  - problem_ref: "..."
    understand: { restated, given, goal, conditions }
    plan: { similar_to, strategy, sub_problems }
    carry_out:
      steps: [{ do, schoenfeld: { what, why, how } }, ...]
      failed_attempts: [...]
    answer: { result, sanity_check }
    hint_level: 2
    look_back: { principle, deep_structure, shared_with, schema_category }
    optional: { newman_diagnosis, ... }
```

### Session 2 — YYYY-MM-DD (continued)

(append-only; new session here, do not edit Session 1)

---

## Phase 3 — Calibrate (opening warmup of next session, by default)

**Date**: YYYY-MM-DD (delay from Phase 2 last session: <hours>; mode: cross-session | same-session-optin | downgraded-to-quiz)

### Confidence (before recall)
- Self-report: 80/100

### Closed-book recall
<user's typed recall, captured before opening chapter>

### Gap calibration
- Expectations covered: 4/5
- Concept_defines covered: 6/8
- Factual errors:
  - "<wrong claim>"
  - "<wrong claim>"
- Coverage: 0.75

### Confidence-accuracy gap
- 80 - 75 = 5  ✓ (well-calibrated)

### Feynman explanation
<user's explain-to-beginner attempt>
- *Feedback*: <jargon flagged, gap notes>

### Concept map
[link or inline mermaid/ascii]

### Self-test
- Q1: ...
  - A: ...
  - correct: yes
- Q2: ...
- Q3: ...

---

## Phase 4 — Apply

### Transfer attempt
- **Domain**: <different domain user picked>
- **Mapping**: <how chapter principle applies>
- **Where it breaks**: <limit case>
- **Result**: success | partial | failure | domain-mismatch

### Spaced re-engagement scheduled
- +1 day: 2026-04-29
- +1 week: 2026-05-05
- +1 month: 2026-05-28

---

## Open threads
- <thing still unclear>
- <topic to follow up>

## Cross-chapter notes
- Connects to Ch.3 because: ...
- Differs from Ch.5's claim about: ...

---

## Spaced retrieval log (filled at +1d, +1w, +1m)

### 2026-04-29 (+1d)
- Prompt: "Name the 3 most important things from Ch.4."
- Answer: ...
- Accuracy: 0.7

### 2026-05-05 (+1w)
- ...
```

## Append-only conventions

- Each session adds a new `### Session N — date` block under Phase 2
- Phase 3 happens once per chapter (re-runs are appended with `### Phase 3 retry — date`)
- Phase 4 transfer attempts can be multiple — each gets its own subsection
- Spaced retrieval entries append over time
- Strikethrough is allowed for explicit corrections to prior entries; do not delete
- Do not edit prior session entries; if a prior answer was wrong, the user revises in a *new* session entry that explicitly references the prior

## Compose mode auto-fill rules

When compose mode runs (end of session or end of phase):

1. Pull session traces from internal state (or transcript if running in Claude Code)
2. Map each captured response to its frontmatter or body section
3. Compute derived fields:
   - `avg_hint_level` from `hint_levels`
   - `avg_answer_length` from session response lengths
   - `closed_book_coverage` from gap_calibration result
   - `confidence_accuracy_gap` from confidence + coverage
   - `session_health.*` flags from detection rules in `references/failure-modes.md`
4. Update `last_session`, increment `sessions`
5. Write file (overwrite if exists for the same date — multiple sessions same day are concatenated within the existing entry block)
6. Update `~/study-journal/books.yml` `chapter_metrics`

## Reading the note for resume

When skill resumes a chapter (next session), read:

1. Frontmatter `status` field — determines next phase
2. Last `### Session N` block — picks up section progress
3. `Open threads` — surfaces things to address
4. `Spaced retrieval log` — checks if any retrieval is due

Do not re-read the entire body unless needed for a Phase 3 calibrate.

## Cross-references

- `references/generative-prompts.md` — content of each Phase
- `references/methods/*.md` — formats for embedded ARQ / Polya / Newman blocks
- `references/calibration.md` — Phase 3 specifics
- `references/citation-format.md` — quote_id schema for citations

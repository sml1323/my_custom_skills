# Calibration — Phase 3 Mechanics

Phase 3 is the **measurement step**. Without it, learning is invisible and self-report substitutes for evidence — and self-reports of understanding are systematically miscalibrated against delayed recall. The skill should not mark a chapter complete without Phase 3. [exact citation pending — the previously cited "Yang 2023, r=0.18" was not externally verifiable; replace with a verified metacomprehension source before next major release.]

## The delay: cross-session by default

Karpicke & Blunt 2011 (Science) compared retrieval practice vs concept mapping. Retrieval won by ~50% on a *delayed* test, but on an *immediate* test the gap was much smaller. The delay is what creates the calibration mechanism.

**Mechanically**: immediate post-reading recall reads from working memory, which is still primed. Delayed recall reads from durable encoding. The two answer different questions:
- Immediate recall = "did you encode the surface?"
- Delayed recall = "did you encode it durably?"

For learning, only the second matters.

**The skill's default**: calibrate runs as the *opening of the next session*, not the tail of the current one. The cross-session gap (hours at minimum, often overnight) is well above the 30-minute floor and is closer to what Karpicke & Blunt 2011 actually measured. This also doubles as `prior_chapter_recall` — the same act covers measurement of Phase 2 *and* spaced retrieval warmup for the new session.

**Same-session calibrate is opt-in only.** The skill checks `phase_2_ended_at` and refuses if `now - phase_2_ended_at < 30 minutes`. The 30-minute floor is the absolute minimum; a real cross-session break (next day) is preferable. Same-session use is opt-in because immediate Phase 3 defeats the purpose: it measures recall from the same encoding pass as Phase 2, not the durable version. Log the run with `calibrate_same_session: true` so the path's usage and outcomes can be reviewed later.

**Stale calibrate (5+ days)**: if `phase_2_ended_at` is older than ~5 days, the chapter has aged out of the calibrate window. Coverage at that point measures long-term retention rather than Phase 2 encoding quality, and comparison to expectations is contaminated by general decay. Downgrade to a 3-question retrieval quiz instead of running the full Phase 3 sequence; log `phase_3_downgraded_to_quiz: true`. Quiz results feed the spaced retrieval log, not the Phase 3 metrics. The user can still request a full Phase 3 explicitly — just don't run one by default at that age.

## The Phase 3 sequence

Run in this order. Do not reshuffle.

### Step 1: confidence_check (BEFORE recall)

> "Before you recall: how confident are you that you can reproduce the chapter's main ideas right now? 0-100."

Capture as `confidence_self_report: <int>`.

This must come before recall, not after. After is contaminated by the recall attempt.

### Step 2: closed_book_recall

> "Without looking at the chapter or your notes: write a 1-page summary covering the main claim, the key concepts introduced, and one example. Take 10 minutes."

Capture as `closed_book_recall: <text>`.

**The user must not open the chapter file.** Enforce by not loading the file into context until after the recall is captured. If running interactively, have the user type the recall first.

### Step 3: gap_calibration

Open the chapter (or chapter note Phase 1 expectations). Compute:

```
expectations_covered = (expectations satisfied in recall) / (total expectations)
concepts_covered = (concept_defines from Phase 2 in recall) / (total concept_defines)
factual_errors = list of wrong claims in recall
coverage = (expectations_covered + concepts_covered) / 2  # or weighted
```

Report as:

```yaml
gap_calibration:
  expectations_covered: 4/5
  concepts_covered: 6/8
  factual_errors:
    - "Said X is necessary; chapter says X is sufficient"
    - "Confused author's position on Y with the position the author was rebutting"
  coverage: 0.75
```

### Step 4: confidence_accuracy_gap

```
confidence_accuracy_gap = confidence_self_report - (coverage * 100)
```

If `gap > 30`: flag illusion signal. Surface to user.

If `gap < -20` (under-confident): rare; surface as positive — usually means user is calibrating well or has imposter signal.

### Step 5: feynman_explain

> "Now: explain [chapter's main concept] as if to someone who knows nothing about [field]. No jargon. Take your time."

Capture as `feynman_explanation: <text>`.

**Read for**:
- Jargon leakage (uses chapter's technical terms without redefining)
- Hand-waving on the part that the recall already revealed as a gap
- Length — too short (< 200 words) often signals surface
- Genuine reformulation vs paraphrase of the chapter

### Step 6: concept_map_build (optional but recommended)

> "Sketch a concept map: nodes for the main ideas, edges for relationships. Include at least one link to a concept from a prior chapter."

User outputs ASCII/mermaid/text-described. Skill does not generate the map (Nesbit & Adesope: g=0.82 for *constructed*, g=0.37 for *consumed*).

### Step 7: self_test_generate

> "Generate 3 questions an exam on this chapter would ask. Then answer them without looking at the chapter."

Capture as:

```yaml
self_test:
  - q: "Why does X imply Y?"
    a: "Because Z..."
    correct: true
  - q: "What's the relationship between A and B?"
    a: "A causes B"
    correct: false  # actually B causes A
    note: "User reversed the causal direction"
```

The questions are queued for spaced re-engagement (Phase 4 of the next session).

---

## Coverage Rubric (grading scale for `recall_coverage`)

`recall_coverage` from Step 3 is computed as a 0.0–1.0 score. Use this rubric to grade consistently across chapters and across users:

| Score | What the recall demonstrates |
|---|---|
| **0.0** | almost no recall — user names the topic only, or less |
| **0.25** | remembers the topic + 1 surface fact; no structure |
| **0.5** | recalls some core concepts, but relations between them are weak or wrong |
| **0.75** | explains most core concepts and their relations, with partial examples |
| **1.0** | explains concepts, relations, and examples; can apply to a new (unseen) case |

Round to the nearest 0.25 in routine grading. Half-steps (0.6, 0.85) are allowed when the recall straddles two bands.

### Pass threshold by book type

`chapter_complete` is gated by `recall_coverage` and (for some types) an additional gate. Step B (diagnostic MCQ) does **not** substitute — it is advisory only.

| Book type | `recall_coverage` threshold | Additional gate |
|---|---|---|
| methodology / argument-driven | ≥ 0.7 | — |
| conceptual | ≥ 0.7 | — |
| problem-driven (math, physics, coding) | ≥ 0.6 | one transfer-problem attempt logged in Phase 4 |
| reference | n/a (PDP not enforced) | — |

### What happens below threshold

- Status stays `phase-3-pending` (or moves back to `in-progress` if the user wants to re-read sections that surfaced as gaps).
- The recall is still logged — the data point matters even when below threshold.
- Schedule a 24-hour retry; do not erase the original attempt.
- Do not soften the result to encourage the user — the rubric exists to break the illusion-of-understanding loop, not to validate it.

### What happens at 1.0

- Promote 1-2 concepts to `evergreen/` extraction immediately while the signal is strong (see `references/citation-format.md` for the extraction format).
- Mark `concept_candidates` rows for the trigger evaluation in `~/study-journal/concepts/` (see SKILL.md "Concept-level tracking").

---

## What "complete" means

A chapter is complete when:

1. Phase 1 done (PKA, prediction, goal_question, expectations, misconceptions captured)
2. Phase 2 done (chapter read; section-break prompts captured; ARQ/Polya invoked as applicable)
3. Phase 3 done (recall + confidence + gap + Feynman + self-test) — **as opening of a later session, or as same-session opt-in with `now - phase_2_ended_at >= 30 min`**
4. Phase 4 transfer attempt logged (success / partial / failure / domain mismatch)

Anything less is `phase-X-pending`. Be explicit about state in `books.yml`:

```yaml
arq:
  current_chapter: 4
  chapter_status:
    1: complete
    2: complete
    3: complete
    4: phase-3-pending  # read but not calibrated
  last_session: 2026-04-28
```

If user says "Ch.4 끝났어" before Phase 3, do not update to complete. Status stays `phase-3-pending` until calibration runs.

---

## Metrics that go on books.yml after each chapter

```yaml
arq:
  chapter_metrics:
    4:
      closed_book_coverage: 0.65
      confidence_self_report: 80
      confidence_accuracy_gap: 15
      hint_levels: [0, 1, 1, 2, 0]
      avg_hint_level: 0.8
      avg_answer_length: 35
      transfer_attempt: success
      session_count: 2
      session_health:
        hint_abuse: false
        illusion: false
        surface: false
        struggle_skip: false
        form_fatigue: false
        echo: false
```

These are the inputs to weekly review and progress dashboard.

---

## Long-term progress signals

Across multiple chapters, watch:

| Trend | Direction | What it means |
|-------|-----------|---------------|
| Closed-book coverage | should rise | core learning signal |
| Confidence-accuracy gap | should narrow toward 0 | calibration improving |
| Avg hint level | should fall | dependency reducing |
| Avg answer length | should hold or rise | engagement quality |
| Transfer success rate | should rise | far transfer developing |
| Spaced retrieval (1w, 1m) | should hit > 60% | durable encoding |

Plot or list these in the weekly review (compose mode output).

If any trend reverses, surface and propose intervention:
- Coverage dropping → reduce session length, more frequent review
- Confidence gap widening → more Phase 3 emphasis; reduce AI explanation
- Hint level rising → enforce productive failure window
- Answer length dropping → push back on short answers; recalibrate effort

---

## Spaced re-engagement (Phase 4)

After a chapter is fully complete, schedule retrieval at:
- +1 day (next session)
- +1 week
- +1 month

Implementation: `books.yml` carries a queue:

```yaml
review_queue:
  - { book: arq, chapter: 4, due: 2026-04-29 }   # +1 day
  - { book: arq, chapter: 4, due: 2026-05-05 }   # +1 week
  - { book: arq, chapter: 4, due: 2026-05-28 }   # +1 month
```

When skill starts a session, check queue. If anything due, run prior_chapter_recall before the new chapter:

> "Today's session has a Ch.4 retrieval due. Take 5 min: name the 3 most important things from Ch.4 without looking. Then we start Ch.5."

Capture results in books.yml:

```yaml
chapter_metrics:
  4:
    spaced_retrievals:
      - { date: 2026-04-29, accuracy: 0.7 }
      - { date: 2026-05-05, accuracy: 0.55 }
      # +1 month pending
```

If a spaced retrieval drops below 50%, re-add chapter to active review (not just spaced). Possibly run a mini calibrate session on it.

---

## Edge cases

- **User can't recall anything in Phase 3**: don't soften. Capture coverage = 0; surface signal; recommend re-reading not from start but from the parts that surfaced as gaps. Schedule a recall retry in 24 hr.
- **User aces Phase 3 (coverage > 90%)**: still capture; this is good but rare. Promote 1-2 concepts to evergreen extraction immediately while signal is strong.
- **Phase 2 ran long, no time for Phase 3 today**: this is the default flow now, not an edge case. Set `status: phase-3-pending` and `phase_2_ended_at: <now>`. End the session. Calibrate runs at next session opening.
- **User wants to redo Phase 3 after seeing the gap**: log the redo (`phase_3_attempts: 2`). Coverage on retry is contaminated; don't replace original; append.
- **User insists on same-session calibrate**: check `now - phase_2_ended_at`. If less than 30 min, refuse with the remaining time plus a one-line reason (working-memory contamination). If at or above 30 min, proceed and log `calibrate_same_session: true`. Do not silently allow this path — the log is what makes the trend visible.
- **Calibrate window has aged out (5+ days)**: downgrade to 3-question retrieval quiz; do not run full Phase 3 by default. If the user explicitly wants full Phase 3 anyway, run it but flag the result in the chapter note: "coverage at this delay is dominated by long-term decay, not Phase 2 encoding."

---

## Why this matters

Without calibration, you're optimizing on the wrong signal. The user feels they understand; the LLM tells them they understand; the chapter note shows completed forms. Months later, the material is gone.

With calibration, the only signal that survives is the one that matters: can you reproduce, transform, and transfer the content. The *feeling* of understanding is well-known to be miscalibrated against actual recall; the *closed-book coverage* number is the signal that survives. [Yang 2023 r=0.18 reference removed pending verification — see top of file.]

This is the single highest-leverage move the skill makes. Everything else can be skipped without breaking learning; Phase 3 cannot.

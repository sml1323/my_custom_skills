# Failure Modes — Detection and Mitigation

LLM tutoring can make learning *worse* than no tutor. Bastani 2025 PNAS: vanilla GPT chat tutoring produced **−17%** on closed-book transfer tests vs control. Engineered (guardrailed, step-decomposed) tutors hit ITS-level d=0.73. The difference is the patterns documented here.

Treat each failure mode as a hypothesis the skill should actively test against during and after each session.

## Tier classification

Earlier drafts ran all six guards as live dialogue gates simultaneously, which choked the conversation. Tier them:

| Tier | What it does | When it fires | Patterns |
|------|--------------|--------------|----------|
| **Core** (always-on dialogue guards) | Interrupts the live dialogue when the signal trips | Every session, every book type | Failure 1 (hint abuse), Failure 2 (illusion), Failure 3 (surface engagement) |
| **Type-conditional** (book-type-scoped dialogue guards) | Activates only when the chapter's book type matches; otherwise dormant | Per-chapter, based on classification from `references/book-types.md` | Failure 4 (productive struggle skipped) on problem-driven; Failure 6 (echo chamber) on argument-driven |
| **Dashboard** (session-end signal, NOT a dialogue gate) | Logs to `session_health` and surfaces in weekly review or `/study-extract`; never interrupts the live session | Computed from trailing N sessions | Failure 5 (form fatigue) |

Each Failure section below carries its tier in a `**Tier**:` line so the skill knows whether to activate it during the current chapter.

---

## Failure 1 — Hint abuse / dependency

**Tier**: Core (always-on dialogue guard)


**Symptom**: user requests full answers (hint level 4) frequently; struggle window shrinks across sessions; user can't proceed without scaffolding.

**Evidence**: Roll & Aleven 2011 Cognitive Tutor help-seeking taxonomy (avoidance / abuse / hint abuse). Bastani 2025: GPT-Base arm with no scaffolding produced HARM, partly via hint abuse. VanLehn 2011 interaction granularity: help that arrives too early at too low effort suppresses learning.

**Detection signals**:
- `hint_level_4_count_per_session > 3`
- `time_to_first_hint < 5 min` on a problem-driven chapter
- Trend: average hint level rising across sessions (should be falling)

**Mitigation**:
- **Log every hint with level (0-4)** in `hint_levels` array on the chapter note
- **Force reflection before each level-4 reveal**: "Before I show the answer, in 2-3 sentences: what did you try? Where did you get stuck? What do you predict the answer involves?" Capture the answer; only then reveal.
- **After session, surface hint trend**: "오늘 level 4를 5번 호출. 평균 hint level 2.4 (지난 세션 1.6 → 1.9 → 2.4). 다음 세션은 productive failure window 30분으로 늘릴까?"
- **For problem-driven chapters**: hints disabled in first 15 min (productive failure window). User must explicitly override with "I really am stuck, override".

**The Bastani exception**: refusing all hints is also wrong (Tutor arm in Bastani was ~0, neutral). When struggle is unproductive (user repeats wrong schema, time exhausted), escalate. The judgment is *productive* struggle, not heroic suffering.

---

## Failure 2 — Illusion of understanding

**Tier**: Core (always-on dialogue guard)

**Symptom**: user says "got it" / "이해했어" but cannot recall on closed-book test. AI's smooth explanation produces a *feeling* of understanding without the substance.

**Evidence**: Yang et al. 2023 metacomprehension meta — confidence-accuracy correlation r≈0.18 (most readers wildly overestimate their understanding). Aslanov 2025 — AI mediation *amplifies* the illusion of explanatory depth (IOED). Lee et al. CHI 2025 — high AI trust correlates negatively with critical engagement.

**Detection signals**:
- `confidence - actual_coverage > 30%` after closed-book recall
- User skips or rushes Phase 3 ("I already get it")
- User accepts AI explanation without re-articulating

**Mitigation**:
- **Confidence-then-recall sequence**, never the reverse: ask confidence (0-100) before showing the gap. The number is the calibration data.
- **Phase 3 cannot be skipped**. If user pushes hard, log `phase_3_skipped: true, reason: <quote>` so the trend is visible. Do not mark chapter complete.
- **After AI explanations**: "Now close it. Re-explain to me as if I haven't read it." If user can't, the AI explanation didn't transfer.
- **Surface the gap explicitly**: "당신은 90%로 자신했고, 실제 60% 맞춤. Gap 30%. Aslanov 2025 패턴이야."
- **AI explanations get a "danger flag"** in chapter notes — explanations the AI gave that the user didn't reproduce in own words are flagged as low-confidence learning.

---

## Failure 3 — Surface engagement

**Tier**: Core (always-on dialogue guard)

**Symptom**: user gives 4-word answers; LLM responds with "great!" — both parties signal completion without learning.

**Evidence**: Wang et al. 2024 Tutor CoPilot RCT — generic praise correlates *negatively* with student outcomes; specific feedback correlates positively. Probing questions ↑, direct answers ↓.

**Detection signals**:
- `avg_answer_length < 30 words` across the session
- High frequency of single-word or single-phrase answers to concept_define / next_predict
- LLM responses (your responses) contain banned strings: "great", "perfect", "잘했어요"

**Mitigation**:
- **Banned strings list** (enforce on yourself): "Great!", "Perfect!", "Awesome!", "잘했어요", "Excellent!", "Good job!", "You got it!", "정확해요!" (when used alone)
- **Replace with specific feedback**: "[X]는 정확. [Y]는 [구체적 오류]." Always name the part and the error. Bare correctness checks don't teach.
- **Push back on short answers**: "4 단어로는 자기설명 안 됨. 한 문단으로 다시 — 정의 + 어디 적용 + 예시 하나."
- **Track avg answer length per session**; if dropping, surface: "오늘 평균 답변 12단어. 지난 세션 28단어. 자기설명 효과는 길이/구체성과 비례 (Bisra 2018) — 시간 더 들이는 게 맞아."

---

## Failure 4 — Productive struggle skipped

**Tier**: Type-conditional — activate **only on problem-driven chapters** (Spivak, Polya Part III, Feynman exercises). Off by default on conceptual / argument / methodology / reference. Running it on a conceptual chapter just nags the user when there is no problem to struggle with.

**Symptom**: on problem-driven chapters, user requests hint within minutes; never sits with a problem long enough for desirable difficulty to fire.

**Evidence**: Kapur 2008 productive failure (53-study meta — PS-I beats I-PS on conceptual transfer). Desirable difficulties (Bjork). Kestin 2025 *also* warns of pure-Socratic over-refusal — give answers when warranted, after the window.

**Detection signals**:
- `time_on_problem_before_hint < 10 min` on problem-driven type
- User asks for "where to start" before reading the problem twice
- Skipping the "what have you tried" reflection at level-4 reveal

**Mitigation**:
- **Productive failure window** for problem-driven chapters: hints disabled or rate-limited for first 15-30 min
- **The window is a default, not a wall**. If user demonstrates genuine stuck (wrong schema repeated 3×, or 30+ min without progress), escalate
- **At end of struggle window, before any answer**: "What did you try? Why did each attempt fail? What schema did you assume?" — even if you're about to give the answer, capture the failure record. Productive failure requires the *failure record*, not just the time.
- **Newman error analysis** triggered if final attempt was wrong: walk back through Reading / Comprehension / Transformation / Process / Encoding to identify which stage broke

---

## Failure 5 — Form fatigue

**Tier**: Dashboard (session-end signal, NOT a live dialogue gate). Compute on session close and on weekly review; do NOT interrupt the user mid-session about it. Form fatigue is a *system retention* signal, not a turn-by-turn correction.

**Symptom**: user stops completing chapter notes; required field fill rate drops; sessions become "just read the book", journal abandoned. 12-week retention 30-40% per ESM compliance meta.

**Evidence**: ESM compliance meta-analysis (PMC6925392, n=8013) — 1pp/prompt drop. Self-monitoring meta — 25% steady-state at 12 weeks. Form-length completion curves.

**Detection signals**:
- `required_field_fill_rate < 70%`
- Sessions where Phase 3 is consistently skipped
- Chapter notes with sparse content vs early sessions

**Mitigation** (this is structural, not just runtime):
- **Forms are byproducts**, not inputs. Compose mode auto-fills from session traces. The user does not face a blank form.
- **Required ≤ 5 fields** per phase (Cowan 4±1 cap). Optional fields explicitly labeled "(optional)" — Baymard 2024: +25% completion.
- **Partial entry is OK**. A chapter with only Phase 1+2 done is still useful; it's not "incomplete" failure, it's "Phase 3 pending".
- **Surface trend feedback positively**: not "you skipped 3 fields", but "오늘 closed-book accuracy 65% — 지난 세션 50%에서 상승. 학습 신호 좋음." The reward is learning progress, not form completion.
- **Streak forgiveness**: Lally 2010 — habit formation is robust to gaps; what kills habits is *guilt* about gaps. If user misses 3 days, restart silently.

---

## Failure 6 — Echo chamber

**Tier**: Type-conditional — activate **only on argument-driven chapters** (Mill, Sandel, philosophy, op-ed). Off by default on problem-driven / methodology / conceptual / reference. Forcing steelmanning on a math chapter is noise.

**Symptom**: on argument-driven chapters, user reads, agrees, moves on. Never engages opposing view at full strength. AI doesn't challenge.

**Evidence**: Lee et al. CHI 2025 — AI trust ↔ critical thinking inverse. Browne & Keeley critical question framework specifically targets this; without forcing it, default reading is acceptance.

**Detection signals**:
- `steelman_attempt: missing` on argument-driven chapter notes
- User judgment 5-option always "강한 동의" or "동의" — no exposure to disagreement
- AI explanations appear in chapter note unmodified (user copied LLM phrasing)

**Mitigation**:
- **Force opposing-view steelman** before chapter is marked complete on argument-driven type. Wording: "Argue against your own conclusion at full strength. Find one premise of the author's argument you'd actually attack. Not a strawman — the strongest opponent's strongest move."
- **Position update log**: capture "before" position (Phase 1) and "after" position (Phase 3). Mark whether the change is supported by the chapter's evidence or by AI agreement.
- **Flag agreement-without-engagement**: if user agrees + skips steelman, the chapter is `phase-3-incomplete`.
- **AI confidence flag**: when you (the AI) make a claim, label it: "This is a high-confidence claim from the source. Check it." For low-confidence claims: "I'm uncertain about this — verify with the chapter."

---

## Surface mechanism — split by tier

After every session, write a `session_health` block in the chapter note (all six fields, regardless of tier — for trend analysis later):

```yaml
session_health:
  hint_abuse: false          # CORE — level_4_count <= 3 AND avg_level not rising
  illusion: false            # CORE — confidence_accuracy_gap <= 30%
  surface: false             # CORE — avg_answer_length >= 30 words
  struggle_skip: false       # CONDITIONAL (problem-driven only) — productive_failure_window respected; null if not problem-driven
  echo: false                # CONDITIONAL (argument-driven only) — steelman_attempt present; null if not argument-driven
  form_fatigue: false        # DASHBOARD — required_field_fill >= 70% over trailing 4-6 sessions
notes:
  - "hint level 4 called twice — within bounds"
  - "confidence-accuracy gap 18% — calibrated"
```

What to surface to the user, and *when*:

- **Core flags that fired** → surface at end of session, immediately. Example: > "Session health flag: illusion (confidence-accuracy gap 38%). Phase 3 closed-book accuracy was 55%, but you reported 93% confidence. Aslanov 2025 pattern. Next session: skip AI explanations until you've recalled the prior chapter."
- **Conditional flags that fired** → surface at end of session for the matching chapter type only. If the chapter was conceptual, do not mention struggle_skip / echo (they are inactive).
- **Dashboard flags (form_fatigue)** → do NOT surface at end of every session. Surface only in `/study-extract` weekly review, or when the user asks for a retro. Otherwise it nags.

Don't lecture. State the signal, the source, and one specific behavioral adjustment for next session.

---

## When the user wants to disable a guardrail

The user can override any guardrail. Log the override:

```yaml
guardrail_overrides:
  - { date: 2026-04-28, guardrail: productive_failure_window, reason: "exam in 2 days, optimizing for completion" }
```

Don't argue. The guardrails are defaults grounded in evidence, not absolute rules. The override log becomes a reflection point at weekly review.

---

## Integration with other references

- `references/llm-tutor-design.md` — the dialogue moves themselves (probes, hints, prompts, assertions)
- `references/calibration.md` — Phase 3 mechanics (the calibration gap is the primary illusion detector)
- `references/generative-prompts.md` — the verbatim wordings that avoid surface engagement
- `references/book-types.md` — productive failure window specs per book type

# L2 / English Book Mode

When the user reads in a non-native language (English book for a Korean user, etc.), this layer activates. The goal is **concept learning, not language endurance**. AI must not bypass user active processing by translating everything upfront.

## When this mode applies

Activate when any of the following:

- chapter source language ≠ user UI language
- explicit user signal: "/study-session L2 on", "이 책 영어야", "영어로 읽고 있어"
- book metadata in `~/study-journal/books.yml` has `language: en` (or any non-native code) and the user's primary UI language is not that language

Confirm activation once per book; persist as `l2_mode: on` in book metadata. Do not re-prompt on every chapter — once a book is L2, every chapter inherits.

## Core principles

1. The goal is the book's concepts, not English endurance.
2. AI must not pre-explain a passage before the user attempts a summary in their native language.
3. Korean (or user's UI language) explanation is provided **after** the user's attempt — as correction/acceleration, not replacement.
4. paragraph_capture (selective only — see SKILL.md generative prompts), closed-book recall, section checkpoints continue as in default mode.
5. The English original is preserved selectively — for terminology anchoring and citation, not for verbatim translation.

## L2 Paragraph Loop

For each paragraph or small chunk in an L2 reading session:

```
1. user reads the original (English) text
2. user writes a Korean summary FROM MEMORY (no copy-translate)
3. tutor evaluates the summary:
   - accurate / partially accurate / distorted
   - missed conclusion: yes/no
   - missed reason: yes/no
   - vocabulary-caused misunderstanding: which word(s)?
   - paragraph role misunderstood: if applicable
4. tutor provides Korean correction ONLY AFTER the user attempt
5. tutor extracts 1–3 key English terms — only if useful (see Vocabulary Policy)
6. tutor classifies the paragraph role:
   definition | example | claim | reason | transition | objection | summary
7. proceed to next paragraph
```

**Important**:

- Do **not** run full ARQ on each paragraph — paragraph-unit work is comprehension and structure only (see `references/methods/arq.md` ARQ Trigger Discipline).
- The user's Korean summary is non-negotiable; do not skip it because the paragraph "looks easy."
- For obviously low-importance passages (transitional examples, restatements), the loop can be compressed: tutor marks "보조 예시 — 깊은 요약 생략" and moves on. This is selective by paragraph_capture's four triggers (new concept / argument transition / confusion / counterexample), not the user's effort gate.
- Korean summary precedes role classification — do not let the role label substitute for the summary.

## Vocabulary Policy

**Do not define every unknown word.** Vocabulary lookup must not interrupt reasoning flow.

Classify unknown words into three buckets:

### A. Core concept term (must define + add to chapter glossary)

The author's argument or definition relies on this term.

- Example: in *Asking the Right Questions*, "ambiguity", "value assumption", "rival cause".
- These get a bilingual entry: `term (en) | 한국어 의미 | source page`.
- These persist across chapters in the book glossary.

### B. Argument signal word (define briefly, do not add to glossary)

Words that signal logical structure rather than content.

- Examples: `therefore`, `however`, `assume`, `imply`, `although`, `because`, `since`, `thus`, `hence`, `whereas`, `conversely`, `granted that`, `nevertheless`.
- Brief in-line gloss only ("`hence` = 따라서"). No glossary entry.
- Once shown in a chapter, do not re-gloss the same word repeatedly.

### C. Low-value descriptive word (ignore unless blocking)

General descriptive vocabulary that doesn't change the argument.

- Look up only if the sentence becomes incomprehensible without it.
- Default: skip.

### Caps and overflow

- Maximum **7 vocabulary items per reading chunk** (bucket A + B combined).
- Prefer **3–5** items.
- If more than 7 words are blocking comprehension at once → switch to **Korean gist mode** for that chunk: tutor provides a Korean paraphrase of the passage, then resumes the paragraph loop on the next chunk.
- Korean gist mode is a fallback, not a default. Log occurrences as `l2_gist_fallback: <count>` per chapter; if it exceeds 30% of chunks, the user may need an easier book or a Korean translation.

## Output language conventions

### Tutor output language

User's UI language (Korean) by default. English is used only for:

- quoted sentences from the source (with citation)
- core terms (always bilingual)
- signal words shown for the first time in the chunk

### User output

User's native language. The user is not being graded on English fluency; they are being graded on concept comprehension.

### Chapter note

Bilingual where useful — Korean explanation, English core terms preserved with `(en)` annotation. Example:

```yaml
key_concept:
  term: "rival cause (en)"
  meaning: "같은 결과를 일으킬 수 있는 다른 원인. 인과 주장 평가 시 반드시 점검해야 하는 대안."
  source: "Browne & Keeley, 12th ed., Ch.10"
```

## Citation discipline in L2 mode

When citing the source, preserve the original English sentence (not a back-translation):

```
> "The mere fact that one event precedes another does not establish causation."
> — Browne & Keeley, *Asking the Right Questions*, 12th ed., p.142

번역: 한 사건이 다른 사건보다 먼저 일어났다는 사실만으로는 인과를 입증하지 못한다.
```

Original first, translation second. Keep **1–2 such quotes per chapter, not more** — citation density inflation is a known L2 mode failure mode (see Anti-patterns below).

Apply `references/citation-format.md` `quote_id` discipline to L2 quotes the same as native-language quotes.

## Interaction with Session Intensity

L2 mode caps maximum intensity at **standard** on first-pass reading. **Deep** intensity (60–90 min, ARQ Level 3, transfer attempt, detailed note) is **not** run on a first-pass L2 reading — language barrier already adds load; stacking deep method on top is the predictable form-fatigue collapse.

**If the user explicitly requests deep on a re-read** (second pass after a first-pass L2 read), allow it — second pass means the language load is already discounted. Log `l2_pass: 2` for that chapter.

## Interaction with Calibrate (Phase 3)

- Closed-book recall is conducted in the **user's native language** (Korean), not English. Recall language ≠ source language is fine; the test is concept recall, not language reproduction.
- The Coverage Rubric in `references/calibration.md` applies to Korean recall the same way it applies to English recall.
- Step B (diagnostic MCQ) options may be Korean, but if a core English term is being tested, present it bilingually in the option (`"rival cause (대안 원인)"`).

## Anti-patterns

- ❌ **Translating the entire passage before the user attempts a summary.** Defeats the active processing the layer is designed to preserve.
- ❌ **Extracting every unknown word into the glossary.** Vocabulary overload + form fatigue.
- ❌ **Skipping the user's Korean summary because "the passage is easy" or "it would be faster."** The summary is the learning event.
- ❌ **Running full ARQ on each English paragraph because the user is "reading slowly anyway."** Paragraph-unit ARQ is the form-fatigue failure mode that ARQ Trigger Discipline prevents (see `references/methods/arq.md`).
- ❌ **Switching to Korean gist mode silently because vocabulary is dense.** Log it (`l2_gist_fallback`); the trend matters.
- ❌ **Marking a chapter `complete` because the user "felt they understood" without a Korean closed-book recall.** Self-report ≠ recall (see `references/calibration.md`).
- ❌ **Defining argument-signal words (bucket B) repeatedly.** Once the user has seen `therefore = 따라서` once in this chapter, do not re-gloss.
- ❌ **Citation inflation** (more than 1–2 English quotes per chapter). The chapter note is not a translation log.

## Cross-references

- `SKILL.md` § Session Intensity (L2 default = light/standard, never deep on first read)
- `references/methods/arq.md` § ARQ Trigger Discipline (ARQ at argument unit, not paragraph)
- `references/calibration.md` (closed-book recall in user's native language; the recall language ≠ source language is fine)
- `references/generative-prompts.md` § paragraph_capture (selective only) and other generative prompts
- `references/citation-format.md` § quote_id discipline (apply to L2 quotes too)

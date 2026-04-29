# Book Types and Default Session Patterns

A book gets exactly one type. Type drives the default session pattern (sequence + timing). The user can override per session, but the type is the starting point.

## The five types

### 1. methodology

**Examples**: Browne & Keeley *Asking the Right Questions*, Polya *How to Solve It*, Cialdini *Influence*, Heuer *Psychology of Intelligence Analysis*.

**What learning looks like**: internalize a method (a checklist, a heuristic set, a sequence of moves), then apply it to external material. The book explains the method; the work happens elsewhere.

**Sessions are not done when the chapter is read**. They're done when the method has been applied to a real outside example at least once.

**Default pattern (35-50 min)**:
- Phase 1 (5 min): PKA + prediction + which external example you'll apply this to
- Phase 2 (25 min): read chapter; trace each method step; mental rehearsal on chosen example
- End session here. Schedule Phase 3 for next sitting.
- Phase 3 (10-15 min, delayed): closed-book method recall; apply method to the chosen external example; identify where it broke
- Phase 4: invoke ARQ or Polya sub-routine on the external example to formalize the application

**Method invocations during reading**:
- ARQ → invoked on external arguments the user brings
- Polya → invoked on external problems

### 2. problem-driven (textbook)

**Examples**: Spivak *Calculus*, Polya Part III worked examples, Feynman exercises, K&R exercises, *Cracking the Coding Interview*.

**What learning looks like**: problem-solving is the work. Reading is preparation; solving is learning.

**Default pattern (40-60 min)**:
- Phase 1 (5 min): problem-type prediction; which schemas/tools you have for this category
- Phase 2 (35-45 min): **productive failure first** — give the user 15-30 min on a problem before any hint. Then worked example if needed. Then a faded-scaffolding follow-up problem.
- Phase 3 (10-15 min, delayed): closed-book problem variant generation; Schoenfeld 3-question reflection on what worked; Newman analysis if the problem was failed

**Method invocations**:
- Polya → primary loop, every problem
- Schoenfeld 3-question → at every transition inside Polya execute
- Newman → if problem was wrong on first attempt

**Special rule**: hints inside the productive failure window (first 15-30 min) require explicit user override. Auto-hint is disabled. The struggle is the desirable difficulty.

### 3. conceptual (textbook)

**Examples**: Feynman *Lectures* body, Griffiths *Introduction to Electrodynamics*, Sapolsky *Behave*, Penrose *Road to Reality*.

**What learning looks like**: concepts accumulate and interlock. You trace derivations, build a mental model, and revisit prior chapters as new concepts depend on them.

**Default pattern (40-60 min)**:
- Phase 1 (5-10 min): PKA dump on the chapter topic; advance organizer if the book provides one; prediction of what the chapter will derive
- Phase 2 (30-40 min): read with single-line derivation tracing (do not skip steps); concept_define on every new term; next_predict on every derivation step (Bisra g=1.37)
- Phase 3 (15 min, delayed): closed-book free recall + Feynman explanation + concept map sketch
- Phase 4: cross-chapter — does this depend on / extend chapter X? If yes, retrieval quiz on X

**Method invocations**:
- Polya → invoked on chapter exercises if present
- Cross-chapter retrieval quiz → mandatory before starting next chapter in same volume

**Special rule**: derivation tracing must be active. If the user reads passively, prompt: "Pause. The last derivation step was [X]. Why does that follow?"

### 4. argument-driven

**Examples**: Mill *On Liberty*, Sandel *Justice*, *Nature* / *Science* op-ed, philosophy papers, policy whitepapers.

**What learning looks like**: claims, assumptions, alternative conclusions. Reading without ARQ-style breakdown leaves you at surface comprehension.

**Default pattern (30-50 min)**:
- Phase 1 (5 min): PKA + your prior position on the issue
- Phase 2 (20-35 min): read with ARQ Core 7 always-on (issue, conclusion, reasons+evidence, assumptions, alternatives, judgment, self-explanation); ARQ Optional 5 conditionally (fallacy if nameable, statistics if cited, etc.)
- Phase 3 (10-15 min, delayed): steelman the opposing view; record your position update before/after
- Phase 4: transfer to a different case the same framework would handle

**Method invocations**:
- ARQ → primary, always-on
- Schoenfeld 3-question → folded into ARQ self-explanation move

**Special rule (echo chamber prevention)**: after the user articulates their judgment, force them to steelman the opposing view at full strength. If they refuse or do it weakly, push back. The session is not complete without this.

### 5. reference / lookup

**Examples**: Polya Part II (heuristic dictionary), K&R reference appendix, regex docs, language reference manuals.

**What learning looks like**: not learning. Lookup. The book is a tool; sessions don't need PDP.

**Default mode**: skip the protocol. The skill enters lookup mode:
- Take the user's question
- Read the relevant entry
- Answer with citation back to the book
- If the user explicitly says "I want to learn this entry", escalate to conceptual or methodology pattern (their choice).

**No chapter notes are generated** by default; the looked-up content is cross-referenced into whichever book they were actively learning.

## Classifying a new book

When the skill encounters a book without a type in books.yml, classify it before the first session.

Heuristics in order:

1. **Title pattern**: "How to ...", "The Art of ...", "<Method> Guide" → likely methodology.
2. **Has worked examples + exercises in every chapter** → problem-driven.
3. **Sequential derivations, building on prior chapters, named in equations** → conceptual.
4. **Argues a thesis, references opposing views, ends with conclusions** → argument-driven.
5. **Alphabetical or topic-indexed entries, no narrative spine** → reference.

If multiple types fit (a book can be hybrid — Polya is methodology + problem-driven + reference depending on Part), classify by Part. Polya:
- Part I (the method): methodology
- Part II (heuristic dictionary): reference
- Part III (worked examples): problem-driven

Confirm with user. Store under `books.yml`:

```yaml
polya:
  path: ~/wiki/tmp_books/polya.pdf
  parts:
    - id: I
      type: methodology
      pages: 1-36
    - id: II
      type: reference
      pages: 37-150
    - id: III
      type: problem-driven
      pages: 151-end
```

## Session pattern overrides

User can override the default pattern for any session:

- "Today I want productive failure first even though this is conceptual" — fine, log it.
- "Skip Phase 1 for this chapter" — accept, but warn once that PKA effect is well-supported.
- "I just want to read; no tutoring" — switch to a reading-only mode that still triggers Phase 3 calibrate at the end.

## Defaults summary

| Type | Phase 1 | Phase 2 | Phase 3 (delayed) | Phase 4 | Method default |
|------|---------|---------|------------------|--------|----------------|
| methodology | PKA + prediction + external example pick | Read + step trace + mental rehearsal | Method recall + apply to example | Formalize ARQ/Polya on example | per-chapter content |
| problem-driven | Type prediction + tool review | **Productive failure** → worked example → fade | Variant generation + Schoenfeld + Newman | Cross-problem schema check | Polya always |
| conceptual | PKA + advance organizer + derivation prediction | Trace single-line, concept_define, next_predict | Free recall + Feynman + concept map | Cross-chapter retrieval | Polya on exercises |
| argument-driven | PKA + prior position | Read + ARQ always-on + Optional triggers | Steelman opposite + position update | Transfer to different case | ARQ always |
| reference | — | lookup → answer → cite | — | cross-ref to active book | — |

## Cross-references

- `references/generative-prompts.md` — verbatim prompts used in each phase
- `references/methods/arq.md` — ARQ Core 7 + Optional 5 + Critical Questions canonical list
- `references/methods/polya.md` — 4-step + Schoenfeld + hint hierarchy
- `references/failure-modes.md` — productive struggle window enforcement, echo chamber prevention
- `references/calibration.md` — delayed retrieval mechanics

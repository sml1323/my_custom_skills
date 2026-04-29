# Polya — Four-Step Problem Solving + Schoenfeld Metacognition

When invoked: chapter contains a problem to solve; user pastes an exercise; problem-driven book type runs Polya as the primary loop. Methodology books that teach Polya (Polya itself) use it during Phase 4 application.

## The four steps (verbatim)

| # | Step | Verbatim prompt |
|---|------|-----------------|
| 1 | Understand | "Restate the problem in your own words. What is given? What is the goal? What are the conditions?" |
| 2 | Plan | "Have you seen a similar problem? Tell me a method you can use to find an answer." |
| 3 | Carry out | "Execute. At each step transition, ask: What am I doing? Why am I doing it? How does it help me?" (Schoenfeld 3-question, sticky) |
| 4 | Look back | "What's the principle that made this work? What other problems share this deep structure?" |

Verbatim wording is from Polya. Do not paraphrase. Translate to Korean naturally for delivery.

## Schoenfeld 3-question (sticky inside step 3)

> "What am I doing? Why am I doing it? How does it help me?"

This is the metacognitive sticky. At every step transition during Carry Out — every time the user moves from one operation to another — re-ask. This prevents drift into mechanical execution.

Korean:
> "지금 무엇을 하고 있나? 왜 하고 있나? 이게 어떻게 도움이 되나?"

Schoenfeld evidence: metacognitive prompts at this granularity is the differentiator between expert and novice problem solving (Schoenfeld 1985, 1992). Without these, students execute procedures without monitoring whether the procedure fits the problem.

## Hint hierarchy (0-4)

Every help moment gets a level. Skill logs the level in the chapter note.

| Level | Description | What you give |
|-------|-------------|---------------|
| 0 | Self-solved | Nothing |
| 1 | Re-read problem | "Read the problem aloud. What's actually being asked?" |
| 2 | Schema lookup | "Have you seen a similar problem? Don't show the solution — just identify the category." |
| 3 | Worked example | Show a similar worked example; user re-attempts |
| 4 | Full reveal | Show solution; require reflection record |

**Productive failure window**: levels 2-4 are *rate-limited* in the first 15-30 minutes for problem-driven chapters. Level 1 (re-read) is always available.

**Level-4 reflection** (mandatory): before showing a solution at level 4, capture:

```
1. What did you try? (each attempt)
2. Why did each attempt fail?
3. What schema did you assume? Was it the wrong fit?
4. What do you predict the solution will involve?
```

After capture, reveal solution. Then ask: "Compare what you predicted to the actual solution. Where did your schema diverge?"

This is from Newman error analysis (see `references/methods/newman.md`) merged with productive failure (Kapur 2008).

## Look back (step 4) — the highest leverage step

Most students skip this. It's the highest-leverage step.

> "What's the principle that made this work? What other problems share this deep structure?"

Push for:
- The *invariant* — the abstract structure stripped of surface details
- One other problem (in this book or another) that shares the same deep structure
- A category name for this problem type

This is where schema formation happens (Chi & Glaser 1981 expert-novice). Surface-feature problems are forgotten; deep-structure schemas transfer.

If user can't name a related problem: "Skip this for now. Add `look_back_pending: true` to the entry. Next session we revisit when you've seen more problems in this category."

## Polya output format inside chapter note

```yaml
polya_logs:
  - problem_ref: "Polya Part III Ex. 7" or "Feynman Vol I Ch.5 Ex.2" or external problem text
    
    understand:
      restated: "..."
      given: "..."
      goal: "..."
      conditions: "..."
    
    plan:
      similar_to: "..."  # prior problem if recognized
      strategy: "..."    # named Polya strategy or other
      sub_problems: ["..."]  # if decomposed
    
    carry_out:
      steps:
        - { do: "introduce variable t", schoenfeld: { what: "변수 도입", why: "대칭성 활용", how: "미분 가능하게" } }
        - { do: "..." }
      failed_attempts:  # productive failure record (kept if any)
        - { tried: "...", why_failed: "...", schema_assumed: "..." }
    
    answer:
      result: "..."
      sanity_check: "단위 일치, 극한 케이스 일치"
    
    hint_level: 2  # 0-4
    
    look_back:
      principle: "..."
      deep_structure: "..."
      shared_with: ["Polya III/Ex.4", "Spivak Ch.3 Ex.7"]
      schema_category: "auxiliary variable / symmetry exploitation"
    
    optional:
      newman_diagnosis: null  # populated if final answer was wrong
      help_seeking_audit: null  # populated if hint_level >= 2
      worked_example_se: null  # if studied a worked example, the 3 SE prompts (Renkl)
      affect: null  # frustration / overconfidence / flow
```

## Common patterns by Polya step

### Understand step — patterns

- User skips, dives into Plan: push back. "Restate first. Don't compute yet."
- User restates by copying the problem verbatim: not restating. Push for own words.
- User's "given" list missing implicit conditions: "What are the *implicit* conditions? Continuity? Boundedness? Domain?"

### Plan step — patterns

- User can't name a similar problem: this is a schema gap. Either drop to level 2 (schema lookup hint) or run reference Polya Part II for a heuristic
- User names strategy too vaguely: "Solve it with calculus" is not a strategy. Push for concrete: "Use auxiliary variable / Substitute / Apply mean value theorem."
- User wants to start computing: "Plan first. What's the *whole* path from given to goal?"

### Carry out step — patterns

- User stops verbalizing Schoenfeld 3-question: re-prompt at every transition. This is the most important sticky.
- User's working drifts from plan: "Pause. Where did you deviate from the plan? Why?"
- User makes a computation error: don't immediately correct. "Sanity check the result. Does this match the goal?"

### Look back step — patterns (highest leverage)

- User: "yeah it works, moving on": NO. "What's the *principle*?"
- User restates the procedure as the principle: push for invariant. "Strip away the calculus / numbers — what's the *abstract* move?"
- User can't find a related problem: log `look_back_pending`, add to next session

## When user gets a problem wrong

Trigger Newman error analysis (see `references/methods/newman.md`). Walk back through the 5 stages. The diagnosis reveals which stage broke (often Comprehension or Transformation, rarely Process).

After Newman: redo the problem from the broken stage forward. Update Polya log with `failed_attempts` populated.

## Polya inside reference mode

Polya Part II is reference, not problem-driven. When user invokes a Polya Part II entry (e.g., "Auxiliary problem"), skill goes to lookup mode:
- Read the entry
- Quote the relevant heuristic
- Answer cross-referencing into whichever active problem the user is solving
- Do not run Polya 4-step on Polya Part II entries themselves; that's not learning, it's lookup

## Anti-patterns

- ❌ **Skipping Understand**: most common error; users want to compute
- ❌ **Plan as one word**: "calculus" or "algebra" not a strategy
- ❌ **Hint level 4 with no reflection record**: defeats productive failure
- ❌ **Skipping Look Back**: highest leverage step; never auto-skip
- ❌ **Schoenfeld 3-question only at start**: must be sticky at every transition
- ❌ **Paraphrasing the 4 steps to "easier" wording**: verbatim or weaker effect

## Cross-references

- `references/methods/schoenfeld.md` — 3-question detail
- `references/methods/newman.md` — error walk-back
- `references/methods/arq.md` — when chapter contains argument, not problem
- `references/failure-modes.md` Failure 1 (hint abuse), Failure 4 (productive struggle)
- `references/book-types.md` — problem-driven default pattern
- wiki concepts: `worked-examples`, `problem-schema`, `schoenfeld-framework`, `productive-failure`

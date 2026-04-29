# Schoenfeld 3-Question Metacognitive Sticky

The single most important metacognitive prompt in problem solving. Verbatim wording matters; do not paraphrase.

## The three questions

> 1. **What am I doing?**
> 2. **Why am I doing it?**
> 3. **How does it help me?**

Korean delivery:
> "지금 무엇을 하고 있나? 왜 하고 있나? 이게 어떻게 도움이 되나?"

## When to apply

Inside Polya step 3 (Carry Out), at every step transition. Not at the start of the problem (that's Plan); not at the end (that's Look Back). At every move *during execution*.

A "transition" means moving from one operation to another:
- Computing X → computing Y
- Applying lemma A → applying lemma B
- Substituting → simplifying
- Trying approach 1 → switching to approach 2

Each transition gets all three questions. Capture answers in the polya_logs `carry_out.steps[i].schoenfeld` block:

```yaml
- { do: "introduce variable t", schoenfeld: { what: "변수 도입", why: "대칭성 활용", how: "미분 가능하게 만들어 극값 추출" } }
```

## Why this works

Schoenfeld 1985, 1992 video-protocol research showed expert problem solvers *spontaneously* ask these questions during execution; novices do not. Novices execute procedures mechanically, drifting from the plan, accumulating computation that doesn't connect to the goal.

The 3 questions force the user to maintain plan-execution coherence: each computation must serve a purpose connected to the goal.

## Patterns

### When user can answer all three crisply

Good. Continue. Mark step as `schoenfeld: aligned`.

### When user can answer "what" and "why" but not "how does it help"

Common. The user is executing a habit move without understanding its purpose for *this* problem. This is a stop signal.

> "Pause here. You're computing [X] but you can't articulate how it gets you to [goal]. Does this step actually serve the plan, or is it a habit?"

Often the answer is "habit" — the user is computing something familiar that doesn't lead to the goal. Re-plan from this step.

### When user can answer "what" only

The user has lost the plan. Stop the computation; redo Plan step.

### When user paraphrases the question instead of answering

> "What am I doing?" → "Solving the problem" — not an answer. Push for the *specific* current operation.

## Anti-patterns

- ❌ Asking only at the start of the problem (that's Plan)
- ❌ Asking only at the end (that's Look Back)
- ❌ Asking once per problem, not per transition
- ❌ Paraphrasing to "what's your plan?" — different question, different effect
- ❌ Letting user skip "how does it help me?" — this is the leverage question

## Schoenfeld outside Polya

The 3-question generalizes. It can be applied to:
- ARQ during Phase 2: at each critical question, "what am I extracting? why this question for this argument? how does it help me evaluate?"
- Conceptual textbook reading at section breaks: "what am I tracing? why this derivation? how does it connect to the chapter goal?"

In these cases, frequency drops to once per major section (not per micro-transition like in Polya). The principle is the same: maintain plan-execution coherence.

## Source

- Schoenfeld 1985 *Mathematical Problem Solving*
- Schoenfeld 1992 "Learning to think mathematically" handbook chapter
- wiki concept: `schoenfeld-framework`

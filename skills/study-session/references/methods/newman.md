# Newman Error Analysis — 5-Stage Walk-Back

When invoked: user gets a problem wrong. Walk back through 5 stages in reverse to identify which stage broke. Diagnosis informs which sub-skill needs work.

## The 5 stages (verbatim)

Anne Newman's research with elementary math students generalizes well to any problem solving. The stages are sequential dependencies — if stage *k* fails, stages *k+1...n* cannot succeed.

| Stage | Question | What it tests |
|-------|----------|---------------|
| 1. Reading | "Read the problem aloud. What words could you not read?" | Decoding |
| 2. Comprehension | "What is the problem asking you to do?" | Understanding semantics |
| 3. Transformation | "How will you find the answer? What method?" | Choosing the right operation/strategy |
| 4. Process | "Show me how you'll work it out. Talk me through each step." | Executing the chosen method |
| 5. Encoding | "Write down the answer in the form the problem asks." | Reporting in the asked-for form |

## How to use

When a user's final answer is wrong, walk *backward* through the stages:

1. Show the user their answer
2. Ask the **Encoding** question first: did they answer in the asked-for form? Sometimes the "wrong" answer is correct but in the wrong form (e.g., decimal asked for fraction).
3. If encoding is fine, walk through **Process**: ask them to re-execute their method. Often the error is a mechanical slip.
4. If process is fine, walk through **Transformation**: did they choose the right method? This is the most common error in problem-driven textbook contexts.
5. If transformation is fine, walk through **Comprehension**: did they understand what was being asked? Often the user was solving a different problem than the one stated.
6. Reading errors are rare in adult learners; usually skipped unless transcription error in problem statement.

## Output: Newman diagnosis

Capture in the polya_logs entry's optional block:

```yaml
optional:
  newman_diagnosis:
    answer_was: "..."
    correct_answer: "..."
    failed_stage: transformation  # 1-5 numeric or named
    diagnosis: "Chose to integrate when separation of variables was needed; missed that the equation was non-separable in the original form"
    correction: "Re-attempt with integrating factor method"
```

## What the diagnosis tells you

| Failed stage | Implication | Next session |
|--------------|-------------|--------------|
| Reading | Vocabulary gap (rare in adults) | Glossary work |
| Comprehension | Reading skill / chapter not understood | Re-read; do concept_define on unclear terms |
| Transformation | Schema gap — no internalized template for this problem type | Worked examples + interleaved practice |
| Process | Computation / procedural slip | More practice problems of same type, focus on careful execution |
| Encoding | Knew the answer but reported wrong | Read problem statement format more carefully; usually one-time |

The most pedagogically rich is **Transformation**. Transformation errors mean the user lacks the schema; this is where worked examples (Renkl) + interleaving (Rohrer) have highest leverage.

## Patterns

- **User claims it's a process error when it's transformation**: "I just made a calculation mistake" — but the calculation they made wouldn't lead to the right answer regardless. Push: "Walk me through the method again. Is the *method* right?"
- **User wants to skip Newman because they know what they did wrong**: capture their self-diagnosis, then walk Newman anyway. Self-diagnosis often misses the actual stage.
- **Transformation failure with confident user**: "I tried integration by parts; you say I should have used substitution" — surface this as a schema/category recognition gap. Add to worked example queue.

## Cross-references

- `references/methods/polya.md` — the 4-step method that frames the problem
- `references/failure-modes.md` Failure 4 (productive struggle skipped) — Newman is invoked *after* the struggle, not during
- wiki concepts: `worked-examples`, `problem-schema`, `productive-failure`

# ARQ — Browne & Keeley Critical Questions Method

When invoked: chapter contains a non-trivial argument; user wants to break down a paper, op-ed, or claim. Argument-driven book type uses ARQ as primary method during Phase 2 of the PDP cycle.

ARQ is *Asking the Right Questions* (Browne & Keeley). The method is a fixed set of critical questions applied to any argument. ARQ is invoked at the **argument unit** (not the paragraph) and at one of four **depth levels** (0–3). Core 7 are the Level 3 fields; Optional 5 fire on triggers within Level 2 or 3. See `## ARQ Trigger Discipline` below for the depth ladder and `## ARQ Trigger Table` for trigger-to-action mapping.

## ARQ Trigger Discipline — when to invoke at what depth

ARQ is invoked at the **argument unit**, not the paragraph. Running ARQ on every paragraph turns a learning method into form fatigue (the irony compounds while reading *Asking the Right Questions* itself).

**Reading unit ladder**:
- *Paragraph*: comprehension only — user summary in target language + role classification (definition / example / claim / reason / transition / objection / summary). No ARQ at this unit.
- *Section*: at section boundary, decide whether the section contains an argument unit. If yes → escalate. If no → continue paragraph loop.
- *Argument unit*: a passage with a clear conclusion supported by reasons. ARQ Level ≥ 1 from here.

**Depth levels** (distinct from `hint_level: 0-4` which is dialogue help — see `references/llm-tutor-design.md`):
- **Level 0**: comprehension only, no ARQ.
- **Level 1**: issue / conclusion / reason candidates only (3 fields, ≤ 2 minutes).
- **Level 2**: targeted ARQ — invoke specific Optional 5 fields based on what the passage actually contains (causal claim → rival_causes; statistics → statistics; ambiguous core term → ambiguous_terms). Core 7 not run in full at this level.
- **Level 3**: full Core 7 (and Optional 5 by trigger). Reserved for chapter-core arguments.

**Level 3 gate** — full Core 7 is allowed only when **at least two** of the following are true for the passage:
- the passage contains a clear conclusion
- the passage gives reasons or evidence
- the passage is central to the chapter
- the user is confused about the reasoning
- the passage contains ambiguity, assumption, statistics, causal claim, or value judgment

**At every section boundary**, the skill must explicitly decide and log:

```yaml
arq_depth_decision:
  section: <section title or §N>
  depth: 0 | 1 | 2 | 3
  reason: <one sentence>
```

This decision is non-optional — silently running Level 3 on every section is the failure mode this discipline prevents.

## ARQ Trigger Table

Use this table to pick the right Level / Optional field when something specific shows up in the passage:

| Trigger in the text | ARQ action |
|---|---|
| Author makes a clear claim | Level 1 — find conclusion |
| `because` / `since` / `therefore` / `thus` / `so` / `hence` / `따라서` / `왜냐하면` appears | Level 1 — separate reason and conclusion |
| Claim + reason appear together | Level 1 — mini ARQ |
| Author tries to persuade the reader | Level 3 candidate — full Core 7 |
| Example is used as support | Level 2 — check evidence quality |
| Ambiguous word or phrase central to the argument | Level 2 — ambiguous_terms (Optional) |
| Value judgment appears | Level 2 — value assumption (Core field 4 partial) |
| Causal explanation appears | Level 2 — rival_causes (Optional) |
| Statistic, study, or number appears | Level 2 — statistics (Optional) |
| Opposing view appears or is excluded | Level 2 — omitted_info (Optional) |
| Section ends | Section checkpoint — decide arq_depth for next section |
| Chapter ends | Chapter-level ARQ synthesis — Level 3 on the chapter-core argument(s) |

## Core 7 (run at Level 3 on each argument unit)

| # | Field | Verbatim prompt | Source |
|---|-------|-----------------|--------|
| 1 | issue | "What is the issue / question at issue?" | ARQ Q1 |
| 2 | conclusion | "What is the author's conclusion?" | ARQ Q1 |
| 3 | reasons + evidence | "Why do they say so? What evidence?" (merged because they are entangled in source text) | ARQ Q2 + Q7, ARG worksheet §I |
| 4 | assumptions (factual + value) | "What facts does the author take for granted? What values does the author take for granted?" | ARQ Q4 + Q5 |
| 5 | alternative_conclusions | "What other reasonable conclusions could the same evidence support?" | ARQ Q11 |
| 6 | judgment (5-option) | 강한 동의 / 부분 동의 / 부분 반대 / 반대 / 판단 보류 | ARG worksheet §VII |
| 7 | self_explanation_one_line | "왜 이게 결론인가?" — one sentence | Dunlosky 2013 targeted SE |

**Why 5-option judgment**: forced-choice prevents the squishy middle of free-form judgment. Bisra g=0.55 self-explanation effect is preserved by the one-line targeted SE in field 7 (van Peppen 2018: generic SE backfires; targeted is the working form).

## Optional 5 (run on trigger)

| Field | Trigger condition | Source |
|-------|-------------------|--------|
| ambiguous_terms | A core term in the argument is multivalued | ARQ Q3 |
| fallacy | A *nameable* fallacy is identifiable (not a vague suspicion) | ARQ Q6 |
| rival_causes | The argument is causal ("X causes Y") | ARQ Q8 |
| statistics | Numbers / statistics cited | ARQ Q9 |
| omitted_info | A specific piece of missing context can be named | ARQ Q10 |

**Critical rule**: Optional fields fire only when the trigger is met. Do not run all 12 fields on every argument. The trigger discipline is what keeps the method usable for daily work (form fatigue prevention, see `references/failure-modes.md`).

The fallacy field especially: do not name fallacies vaguely. Either you can name the specific fallacy and point to the move that fits it, or the field is empty. False-positive fallacy hunting hurts more than skipping.

## Verbatim wording in delivery

Translate the prompt to Korean for the user but preserve the structure of Browne-Keeley's questions. Do not invent shortened versions.

Example delivery for Core 7:

```
### 이슈
무엇을 다투는가? (저자가 답하려는 질문)

### 결론
저자의 결론은?

### 이유 + 근거
왜 그렇게 말하는가? 어떤 근거를 제시하는가?

### 가정
- 사실 가정: 저자가 당연시하는 사실?
- 가치 가정: 저자가 당연시하는 가치?

### 대안 결론
같은 근거로 다른 합리적 결론이 가능한가?

### 내 판단 (5지선다)
강한 동의 / 부분 동의 / 부분 반대 / 반대 / 판단 보류

### 자기설명 한 줄
왜 이게 결론인가? (한 문장)
```

## How ARQ fits inside PDP

ARQ is invoked from inside Phase 2 (during reading). The session protocol decides *when* to invoke it; ARQ decides *how*.

For argument-driven books (Mill, Sandel, ARQ itself):
- Invoke ARQ Core 7 on each major argument in the chapter
- Do not run ARQ on the chapter as a whole; run it on each argument separately
- Optional 5 fires conditionally per argument
- Output: one ARQ block per argument, embedded in chapter note Phase 2 section

For methodology books that teach ARQ (the ARQ book itself):
- Phase 2 reads the chapter explaining a critical question
- Phase 4 (apply): user picks an external article and runs ARQ on it
- The applied ARQ goes in the chapter note as the "application artifact"
- This is the test of whether the method has been internalized

For other book types:
- ARQ is invoked ad-hoc when the chapter contains an argument worth breaking down
- Sometimes 1 ARQ in a chapter, sometimes none

## Anti-patterns

- ❌ **Running all 12 fields on every argument**. Form fatigue. Use trigger discipline for Optional 5.
- ❌ **Verbatim summary of the author's argument in the "이유 + 근거" field**. Verbatim summary is low-utility per Dunlosky. Restate in your own words.
- ❌ **Fallacy hunting without specific naming**. Either the fallacy is namable and the move identifiable, or skip the field.
- ❌ **Free-form judgment instead of 5-option**. The forced choice is the commitment device.
- ❌ **Skipping self_explanation_one_line because "the conclusion already explains itself"**. The point is the user articulating the *because*, not paraphrasing the conclusion.

## Failure modes specific to ARQ

- **Echo chamber**: user agrees with author, judgment 5 is "강한 동의" every time. Mitigation: force opposing-view steelman before chapter complete (see `references/failure-modes.md` Failure 6).
- **Surface restating**: "이슈" field is just the author's first sentence. Push back: "what's the question the author is *trying to answer*, not the topic?"
- **Assumption missing the value**: factual assumptions are easy; value assumptions are usually skipped. Specifically prompt: "한 줄 — 저자가 무엇을 *선*으로 가정하나?"

## ARQ output format inside chapter note

```yaml
arq_extracts:
  - target: "Section 4.2 — author's argument for X"
    issue: "..."
    conclusion: "..."
    reasons_evidence: "..."
    assumptions:
      facts: "..."
      values: "..."
    alternative_conclusions: "..."
    judgment: "부분 동의"
    self_explanation_one_line: "..."
    optional:
      ambiguous_terms: null
      fallacy: null
      rival_causes: "..."  # fires because argument is causal
      statistics: null
      omitted_info: null
    citations:
      - { quote_id: rc-1, page: 142, cited_text: "..." }
```

## Cross-references

- `references/methods/polya.md` — when chapter has a problem, not an argument
- `references/failure-modes.md` Failure 6 (echo chamber) — argument-driven sessions need steelman
- `references/generative-prompts.md` — Phase 1 PKA + prior position; Phase 3 steelman
- `references/citation-format.md` — quote_id discipline

# Generative Prompts — Verbatim Library

Verbatim wording matters. Bisra 2018 found "anticipate" prompts at g=1.37 vs generic "summarize" at near-null. Use the exact words below; do not paraphrase. Translate to Korean only when delivering to the user (not when planning internally).

Each prompt has:
- **Purpose**: what learning move it serves
- **Verbatim (EN)**: the canonical English wording (from the source paper)
- **Korean delivery**: a faithful translation for the user
- **Trigger**: when to use it
- **Avoid**: common mistake versions

---

## Phase 1 — Pre-reading

### pka_dump

- **Purpose**: activate prior knowledge before reading; surface misconceptions early
- **Source**: Hattan, Alexander, Lupo 2024 RER — open-ended PKA most evidenced
- **Verbatim**: "Write everything you already know about [topic]. Three minutes. No editing."
- **Korean**: "[주제]에 대해 알고 있는 걸 다 써봐. 3분. 편집하지 말고."
- **Trigger**: first move of every Phase 1 (except reference type)
- **Avoid**: "Tell me your background" (closed); "What is X?" (yields textbook answer not personal knowledge)

### prediction

- **Purpose**: prime expectation; create prediction error opportunity
- **Source**: Pressley & Afflerbach 1995 (skilled-reader protocol)
- **Verbatim**: "Predict what this chapter will argue, prove, or teach."
- **Korean**: "이 챕터가 무엇을 주장/증명/가르칠지 예측해봐."
- **Trigger**: after pka_dump, before reading
- **Avoid**: "What do you think this is about?" (vague); accepting passive "I don't know" — push for at least one concrete prediction

### goal_question

- **Purpose**: focus reading, create retrieval cue
- **Source**: gradual release / inquiry pedagogy
- **Verbatim**: "What's one specific question you want answered by the end of this chapter?"
- **Korean**: "이 챕터를 다 보면 답을 얻고 싶은 구체적 질문 하나가 뭐야?"
- **Trigger**: after prediction
- **Avoid**: "What's your goal?" (too abstract)

---

## Phase 2 — During-reading

### concept_define

- **Purpose**: targeted self-explanation in own words; high-leverage retention move
- **Source**: Bisra 2018 self-explanation meta — g=0.87 for "conceptualize"
- **Verbatim**: "Define [concept] in your own words. Where does it apply? Give one example."
- **Korean**: "[개념]을 본인 말로 정의해봐. 어디에 적용되나? 예시 하나."
- **Trigger**: every new technical term in the section; every chapter section break
- **Avoid**: "Did you understand X?" (yields yes/no, no learning); "Summarize section 3" (verbatim summary, low utility)

### next_predict

- **Purpose**: anticipate next derivation/argument step before reading it
- **Source**: Bisra 2018 — anticipatory g=1.37 (highest in meta)
- **Verbatim**: "Predict what the next [step / paragraph / proof line] will conclude. Why?"
- **Korean**: "다음 [단계/문단/증명줄]이 무엇을 결론낼지 예측해봐. 왜?"
- **Trigger**: at section break in conceptual/problem-driven; before each derivation step
- **Avoid**: revealing the answer in the prompt ("the next step uses calculus, what will it conclude?")

### monitoring_check

- **Purpose**: detect comprehension failure; force the user to slow on confusion
- **Source**: Pressley & Afflerbach 1995; Block & Pressley monitoring research
- **Verbatim**: "Paraphrase the last paragraph. If you can't, mark it as a confusion point."
- **Korean**: "마지막 문단을 본인 말로 다시 설명해봐. 못하면 confusion으로 표시."
- **Trigger**: every 2-3 paragraphs; when user has been quiet for 5+ min
- **Avoid**: "Are you following?" (yes-bias)

### selective_annotation

- **Purpose**: capture 1-2 highest-leverage claims per page; do NOT highlight more (Dunlosky 2013)
- **Verbatim** (instruction to user): "Mark the 1-2 claims on this page that, if removed, would break the chapter's argument. Not 5. Not 10."
- **Korean**: "이 페이지에서 빠지면 챕터 논증이 무너지는 핵심 주장 1-2개만 표시. 5개도 10개도 아닌."
- **Trigger**: each page with annotatable content
- **Avoid**: highlighting whole sentences; highlighting more than 2 per page (inference accuracy drops per Dunlosky)

---

## Phase 3 — Post-reading (DELAYED — not immediate)

### closed_book_recall

- **Purpose**: actual learning measurement (vs self-report)
- **Source**: Karpicke & Blunt 2011 Science; Yang 2023 metacomprehension meta
- **Verbatim**: "Without looking at the chapter, write a 1-page summary covering: the main claim, the key concepts introduced, and one example. Take 10 minutes."
- **Korean**: "챕터를 보지 말고, 1페이지 요약을 써봐: 핵심 주장, 새로 등장한 핵심 개념들, 예시 하나. 10분."
- **Trigger**: at the start of Phase 3 — by default this is the opening of the *next* session (cross-session gap = the delay). Same-session opt-in only when `now - phase_2_ended_at ≥ 30 min`.
- **Critical**: do not let the user open the chapter file. If running in chat, take their typed recall before showing any chapter content.
- **Avoid**: shortening to less than 5 minutes; allowing peeking

### gap_calibration

- **Purpose**: compare self-recall to chapter; surface what was missed/wrong
- **Source**: Yang 2023 — calibration is what delayed retrieval repairs
- **Procedure**:
  1. After closed_book_recall is captured, open the chapter
  2. List expectations (from Phase 1) and check which were covered
  3. List concept_defines (from Phase 2) and check which appear in recall
  4. Identify wrong claims in recall (factual errors)
  5. Output: `{ missed: [...], wrong: [...], coverage: 0-1 }`
- **Korean delivery**: "비교해보자. 빠진 것: [...]. 틀린 것: [...]. Coverage: 65%."
- **Critical**: do not soften the gap. Yang 2023 r=0.18 means most users overestimate their understanding by 30-50%.

### confidence_check

- **Purpose**: measure confidence-accuracy gap; detect illusion of understanding
- **Source**: Aslanov 2025 (AI mediation amplifies IOED); Yang 2023
- **Verbatim**: "Before I show you the gap analysis: how confident are you that your recall is accurate? Give a percentage 0-100."
- **Korean**: "Gap 보여주기 전에 묻는다: 본인 recall이 정확하다고 얼마나 자신해? 0-100으로."
- **Trigger**: after closed_book_recall, BEFORE gap_calibration
- **Output**: `confidence_accuracy_gap = confidence - actual_coverage`. If > 30%, surface as illusion signal.

### feynman_explain

- **Purpose**: teaching expectancy + delivery effect; high-leverage delayed retention
- **Source**: Fiorella & Mayer 2014 — d=0.79 delayed for explanation with delivery
- **Verbatim**: "Explain [main concept] as if to a beginner who knows nothing about [field]. No jargon."
- **Korean**: "[핵심 개념]을 [분야]를 모르는 초보자에게 설명한다고 생각하고 말해봐. 전문용어 없이."
- **Trigger**: after gap_calibration, on the highest-stakes concept of the chapter
- **Output**: capture full explanation. Read for jargon leakage and gaps. Push back on anything that requires prior knowledge to follow.

### concept_map_build

- **Purpose**: organize chapter's concepts into a structure; relate to prior chapters
- **Source**: Nesbit & Adesope 2006 — g=0.82 for *constructing* (but only g=0.37 for studying provided maps)
- **Verbatim**: "Sketch a concept map: nodes for the main ideas, edges for relationships. Include at least one link to a concept from a prior chapter."
- **Korean**: "Concept map 그려봐: 노드는 핵심 아이디어, 엣지는 관계. 이전 챕터 개념과 연결되는 link 최소 1개."
- **Trigger**: after feynman_explain; optional but high-value
- **Output**: ASCII art, mermaid, or text description (link to file if user sketches in tool)
- **Critical**: must be user-constructed. Skill providing a map yields the lower-effect study mode.

### self_test_generate

- **Purpose**: user-generated retrieval items; test-generation effect; preview future retrieval
- **Source**: Roediger retrieval lit; user-generated items > provided items
- **Verbatim**: "Generate 3 questions an exam on this chapter would ask. Then answer them without looking."
- **Korean**: "이 챕터로 시험 보면 나올 만한 문제 3개 만들어봐. 그리고 보지 말고 답해."
- **Trigger**: end of Phase 3
- **Output**: `[{q, a, correct}]` triples; the q's get added to next session's spaced re-engagement queue

---

## Phase 4 — Cross-chapter / Apply

### prior_chapter_recall

- **Purpose**: spaced retrieval of prior chapter; opens next session
- **Source**: Cepeda 2008 spacing meta; retrieval-practice
- **Verbatim**: "Before we start chapter [N+1]: name the three most important things from chapter [N]. No looking."
- **Korean**: "Ch.[N+1] 시작 전에: Ch.[N]에서 가장 중요한 3가지를 답해. 보지 말고."
- **Trigger**: start of every session that follows a completed chapter
- **Output**: capture answer; compare to prior chapter's expectations; log result

### interleave_compare

- **Purpose**: connect related chapters / problem types; deep-structure recognition
- **Source**: interleaving meta (d=0.83-1.21 for math/physics)
- **Verbatim**: "How does this chapter's [main idea / method / problem type] relate to chapter [X]? Same? Different? Where do they diverge?"
- **Korean**: "이 챕터의 [핵심 아이디어/방법/문제 유형]이 Ch.[X]와 어떤 관계? 같음/다름? 어디서 갈리나?"
- **Trigger**: after a chapter completes that has a related prior chapter
- **Output**: a 3-5 sentence comparison; goes into both chapters' "cross-references" sections

### transfer_attempt

- **Purpose**: far transfer; the most stringent learning evidence
- **Source**: Bisra 2018 g=0.53 transfer; Bartz transfer literature
- **Verbatim**: "Apply [chapter's principle / method] to a different domain you know — work, hobby, prior reading. Where does it map? Where does it break?"
- **Korean**: "[챕터의 원리/방법]을 본인이 아는 다른 도메인 — 일/취미/이전에 읽은 것 — 에 적용해봐. 어디서 매핑되고 어디서 깨지나?"
- **Trigger**: end of every fully-completed chapter (Phase 1-3 done)
- **Output**: capture the transfer attempt + result (success / partial / failure / domain mismatch). Successful transfers become evergreen note candidates.

---

## Wording rules

1. **Use the verbatim source wording in the planning prompt to yourself**, then translate to Korean naturally for the user. Do not invent new wording.
2. **Avoid yes/no framing**. "Did you understand X?" yields yes-bias. Replace with "Define X."
3. **Avoid hedge language**. "Maybe try to predict..." weakens the prompt. Use imperative.
4. **Avoid generic praise after answers**. "Great!" / "잘했어요!" / "Perfect!" are banned. Replace with specific feedback (see `references/llm-tutor-design.md`).
5. **Push back on short answers**. If user gives 4-word concept_define, that's not a definition. "More — give me one full sentence and an example."

## Anti-patterns (DO NOT use)

- ❌ "Summarize the chapter." (verbatim summary, low utility per Dunlosky)
- ❌ "Reread the section." (low utility, default behavior we're trying to displace)
- ❌ "What's the main point?" (vague)
- ❌ "Highlight the important parts." (highlighting hurts inference per Dunlosky)
- ❌ "Tell me what you learned." (forces self-report; we want closed-book recall)
- ❌ "How confident are you that you understand?" — instead, measure with retrieval

## Quick sequence reference

A typical 45-min Phase 2 + Phase 3 (split across two sittings) hits:

```
Phase 1 (5 min):
  pka_dump
  prediction
  goal_question

Phase 2 (25-30 min, single block):
  every section break:
    concept_define OR next_predict (alternate)
    monitoring_check (every 2-3 paragraphs)
  selective_annotation (rolling, 1-2 per page)
  ARQ or Polya invocation as content calls for it

[END PHASE 2 — session ends; status: phase-3-pending]

Phase 3 (15 min, opens the *next* session by default):
  closed_book_recall
  confidence_check
  gap_calibration
  feynman_explain
  concept_map_build (optional, recommended)
  self_test_generate

Phase 4 (5 min, anytime after Phase 3):
  transfer_attempt
  schedule prior_chapter_recall for next session
```

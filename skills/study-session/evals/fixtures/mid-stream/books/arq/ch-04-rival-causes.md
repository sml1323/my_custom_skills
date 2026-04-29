---
title: ARQ Ch.4 — Are There Rival Causes?
book: arq
chapter: 4
type: methodology
status: phase-2-complete
sessions: 1
created: 2026-04-26
last_session: 2026-04-26
hint_levels: [0, 1, 1, 0]
avg_hint_level: 0.5
avg_answer_length: 38
closed_book_coverage: null
confidence_self_report: null
confidence_accuracy_gap: null
session_health:
  hint_abuse: false
  illusion: false
  surface: false
  struggle_skip: false
  form_fatigue: false
  echo: false
review_queue: []
related_chapters:
  - { book: arq, chapter: 8, relation: "depends-on" }   # statistics chapter
---

# Ch.4 — Are There Rival Causes?

## Phase 1 — Plan
- **PKA dump**: 인과 추론에서 흔한 함정. correlation ≠ causation. 다른 원인 가능성을 빠뜨리면 잘못된 결론.
- **Prediction**: 챕터가 X causes Y 주장을 어떻게 challenge하는지 보여줄 거. 대안 원인 후보 (chance, reverse, common cause, confound) 정리.
- **Goal question**: rival cause를 빠짐없이 뽑아내는 체크리스트가 있는가?

### Expectations (skill-generated)
- User can name 5 categories of rival causes (chance, reverse causation, common cause, third variable, selection)
- User can identify when a stated cause is actually a confound
- User can apply rival-cause checklist to an external news claim
- User can distinguish post hoc fallacy from spurious correlation

### Misconceptions to watch
- User confuses correlation with causation in their own examples
- User over-applies rival-cause skepticism (treats every causal claim as suspect, missing strong evidence)

---

## Phase 2 — During reading

### Session 1 — 2026-04-26 (avg hint 0.5, avg answer 38 words)

#### Section 4.1 — Pages 61-65
- **concept_define [rival cause]**: 사용자가 "같은 증거가 지지하는 다른 원인"으로 정의. 본인 예시: 학생 시험점수 ~ 공부시간; rival = 가정 환경, 사전 지식. ✓
  - *Feedback*: 정의 정확. 예시에서 "사전 지식"은 *common cause* 하위유형 — 이름을 명시하면 더 정확.

#### Section 4.2 — Pages 66-71
- **next_predict [post hoc fallacy 다음 등장]**: 사용자 예측 — "X가 Y보다 먼저 일어났다고 X가 Y의 원인이라 결론"
  - *actual*: 정확
  - *gap*: 없음

- **selective_annotations**:
  - p.68 — "Confounding variable explains both X and Y" (high-leverage)
  - p.70 — "Reverse causation is often invisible without temporal data" (high-leverage)

#### Section 4.3 — Pages 72-75
- **monitoring_check**: 사용자가 chance variation과 systematic confound 차이를 paraphrase 못함 → confusion 마크
- *Skill follow-up*: chance = sampling noise, confound = causal third variable. 사용자가 다시 정의 — 정확.

### ARQ extract — Section 4.2's example argument
```yaml
arq_extracts:
  - target: "Section 4.2 — author's argument that 'the new study shows X causes Y'"
    issue: "X와 Y 사이의 인과 방향성"
    conclusion: "X causes Y는 single study evidence로 결론짓기 약함"
    reasons_evidence: "인용 연구는 cross-sectional, 시간 순서 미상"
    assumptions:
      facts: "측정 도구의 신뢰성"
      values: "intervention worth pursuing if causal"
    alternative_conclusions: "Y → X (reverse), Z causes both X and Y (common cause), chance"
    judgment: "부분 동의"
    self_explanation_one_line: "저자는 single study causal claim에 항상 4가지 대안을 점검하라고 주장 — 그게 rational base rate"
    optional:
      rival_causes: "common cause Z — socioeconomic status가 X와 Y 모두에 영향"
    citations:
      - { quote_id: rc-1, page: 142, printed_page: "p.138", cited_text: "..." }
```

---

## Phase 3 — Calibrate (DELAYED)

*상태: 미진행. Phase 2 종료 시각으로부터 30+ 분 경과 후 진행 예정.*

---

## Open threads
- common cause vs confound 차이 — 다음 세션에서 확인
- Ch.8 (statistics) 의 selection bias와 어떻게 연결되는지

---
name: study-verify
description: |
  Phase-level comprehensive verification for /study sessions. Generates a
  from-scratch exercise covering all concepts learned in a phase, then verifies
  the user's solution. Use when: user says "/study-verify", "검증해줘", "채점해줘",
  "phase 검증", "종합 테스트", or wants to test their understanding of a completed
  phase. Also trigger when a user finishes a study phase and wants to confirm
  they really understood everything before moving on.
---

# /study-verify — Phase Comprehensive Test

Phase 단위 종합 검증. 해당 Phase에서 배운 모든 개념을 **처음부터 새로 작성**하게 해서
진짜 이해했는지 테스트합니다. 기존 코드 복사/수정이 아닌 백지 상태에서 시작.

## Usage

```
/study-verify {topic} [phase_number]
```

- `topic`: study 토픽 (study/ 아래 폴더명)
- `phase_number`: 검증할 phase 번호 (생략 시 가장 최근 완료된 phase)

## Flow

### 1. 상태 확인

Read `study/{topic}/plan.md`:
- 완료된 task 목록 파악 (`- [x]`)
- phase_number 생략 시: 모든 task가 완료된 가장 최근 phase 선택
- 해당 phase의 task가 전부 완료되지 않았으면 경고 후 진행 여부 확인

### 2. 종합 과제 생성

해당 Phase의 모든 task에서 배운 개념을 **하나의 과제**로 통합.

과제 설계 원칙:
- 학습한 토픽과 유저 프로젝트 도메인에 맞는 실용적 시나리오
- 이전 exercise와 다른 새로운 시나리오 (단순 반복 방지)
- Phase의 모든 핵심 개념을 자연스럽게 포함
- 명확한 완료 기준 제시 (체크리스트 형태)

출력 형식:
```
🧪 Phase {N} 종합 테스트

📋 시나리오: {한 문장 설명}

✅ 완료 기준:
- [ ] {개념 1 관련 기준}
- [ ] {개념 2 관련 기준}
- [ ] {개념 3 관련 기준}
```

파일 scaffolding:
```bash
mkdir -p study/{topic}/phase-{N}-verify
```
빈 파일 생성: `study/{topic}/phase-{N}-verify/verify.{ext}`
— 이전 코드 복사 없이 빈 파일. 처음부터 작성하는 것이 목적.

"파일을 만들어뒀어요: `{path}`. 처음부터 작성해보세요!"

**Then STOP. Wait for user.**

### 3. 힌트 제공 (요청 시만)

유저가 막히면 힌트 에스컬레이션 적용:
1. 방향 힌트 ("~를 먼저 정의해보세요")
2. 좁은 힌트 ("~에서 ~를 사용하세요")
3. 부분 스캐폴드 (구조만, 구현은 비움)
4. 전체 설명 (3회 이상 실패 또는 명시적 요청 시)

### 4. 검증

유저가 완료하면:

**자동 검사 (안전):**
- 파일 존재 확인
- Syntax check (`python -m py_compile` / `node --check` / etc.)
- 완료 기준별 핵심 패턴 Grep (imports, class, function 등)

**LLM 검토:**
- 완료 기준 체크리스트 하나씩 평가
- 각 개념의 올바른 사용 여부
- 코드 품질 (구조, 네이밍, 관용적 사용법)

**유저 코드 자동 실행 금지. Syntax check만 가능.**

### 5. 결과 리포트

```
🧪 Phase {N} 종합 테스트 결과

{PASS ✅ | NEEDS_WORK 🔄}

체크리스트:
✅ {기준 1} — {한줄 코멘트}
✅ {기준 2} — {한줄 코멘트}
❌ {기준 3} — {무엇이 부족한지}

💪 잘한 점: {구체적 칭찬}
💡 개선점: {있으면}
```

### 6. 기록

Append to `study/{topic}/log.md`:
```markdown
### Phase {N} 종합 테스트 — {YYYY-MM-DD}
- 결과: {PASS|NEEDS_WORK}
- 체크리스트: {통과}/{전체}
- 메모: {한줄 요약}
```

- PASS → "다음 Phase로 넘어가도 좋습니다! `/study continue`로 이어가세요."
- NEEDS_WORK → 부족한 개념 짚어주고 재시도 권유. 재시도 시 같은 시나리오 유지.

# Expected Output: Python 데코레이터

아래는 example-input.md를 `/vault-note`로 처리했을 때 기대되는 출력입니다.

---

```md
---
title: "Python 데코레이터 — 개념, 패턴, 사용법"
created: "2026-03-30 10:30:00"
source: "session"
source_type: "conversation"
tags:
  - python
  - decorator
  - design-pattern
related:
  - "[[python 매직메서드]]"
---

# Python 데코레이터 — 개념, 패턴, 사용법

## Summary

> [!IMPORTANT]
> 데코레이터는 다른 함수를 감싸서 동작을 수정하는 함수. `@` 구문으로 사용하며, 로깅, 인증, 캐싱, 재시도 등 횡단 관심사(cross-cutting concerns)에 활용. 항상 `@functools.wraps`를 함께 쓸 것.

## Key Insights

- 데코레이터는 함수를 인자로 받아 새 함수를 반환하는 고차 함수
- `@functools.wraps(func)`를 안 쓰면 원래 함수의 메타데이터가 사라져 디버깅이 어려워짐
- 클래스 기반 데코레이터는 `__call__` 구현으로 상태 유지 가능하지만, 대부분 함수 기반으로 충분
- 가장 흔한 사용처: 로깅, 인증 확인, 캐싱(`@lru_cache`), 재시도 로직

## Details

### 기본 패턴

함수 기반 데코레이터의 표준 구조:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 함수 호출 전 로직
        result = func(*args, **kwargs)
        # 함수 호출 후 로직
        return result
    return wrapper
```

> [!TIP]
> 데코레이터를 만들 때 `@wraps(func)`를 항상 추가하세요. 안 쓸 이유가 없습니다.

### 클래스 기반 데코레이터

상태를 유지해야 할 때(예: 호출 횟수 추적) 클래스 기반이 유용:

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
```

> [!NOTE]
> 클래스 기반은 상태 관리가 필요할 때만 사용. 대부분은 함수 기반으로 충분.

## Sources

- Claude 대화 세션 (2026-03-30)

## Related Notes

- [[python 매직메서드]]
```

---

## Verification Checklist

이 출력이 올바른지 확인할 포인트:

- [ ] 모든 frontmatter 스칼라 값이 따옴표로 감싸져 있는가
- [ ] callout이 NOTE, TIP, IMPORTANT, WARNING, CAUTION 중 하나인가
- [ ] `related`의 [[]] 링크가 실제 볼트에 존재하는 파일과 매칭되는가
- [ ] tags가 lowercase kebab-case인가
- [ ] 내용이 한국어로 작성되었는가 (입력이 한국어이므로)
- [ ] 빈 섹션(Open Questions, Action Items)이 생략되었는가

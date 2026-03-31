# Example Input: Python 데코레이터 대화

아래는 `/vault-note`에 입력할 수 있는 대화 내용의 예시입니다.

---

**사용자**: 파이썬 데코레이터가 정확히 뭐야? 언제 써야 해?

**클로드**: 데코레이터는 다른 함수를 감싸서 그 함수의 동작을 수정하는 함수입니다. `@` 구문으로 사용합니다.

가장 흔한 사용 사례:
1. **로깅**: 함수 호출 시 자동으로 로그를 남기고 싶을 때
2. **인증 확인**: API 엔드포인트에서 사용자 인증을 확인할 때
3. **캐싱**: `@functools.lru_cache`로 함수 결과를 캐싱
4. **재시도 로직**: 네트워크 요청 실패 시 자동 재시도

기본 패턴:
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("함수 호출 전")
        result = func(*args, **kwargs)
        print("함수 호출 후")
        return result
    return wrapper

@my_decorator
def hello():
    print("hello")
```

**사용자**: `functools.wraps`는 왜 쓰는 거야?

**클로드**: `functools.wraps`를 안 쓰면 데코레이터가 원래 함수의 메타데이터(이름, docstring)를 덮어씁니다. 디버깅할 때 `hello.__name__`이 `wrapper`로 나오면 혼란스럽죠.

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # 이걸 추가
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

항상 `@wraps(func)`를 쓰세요. 안 쓸 이유가 없습니다.

**사용자**: 클래스 기반 데코레이터도 있어?

**클로드**: 네, `__call__` 메서드를 구현하면 됩니다. 상태를 유지해야 할 때 유용합니다.

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
```

하지만 대부분의 경우 함수 기반 데코레이터로 충분합니다. 클래스 기반은 호출 횟수 추적이나 상태 관리가 필요할 때만 쓰세요.

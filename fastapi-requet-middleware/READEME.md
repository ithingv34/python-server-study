## Contextvars

Python의 ContextVar는 컨텍스트 관리 블록 내에서 컨텍스트별 데이터를 저장하고 액세스하는 방법을 제공하는 Python 3.7에 도입된 클래스이다. 이를 통해 함수, 코루틴과 같은 특정 컨텍스트 범위 내에서 액세스할 수 있는 변수를 만들 수 있다

**예시**

```
import asyncio
import contextvars

# Define a context variable
user_var = contextvars.ContextVar("user")


async def greet():
    # Access the context variable
    user = user_var.get()
    print(f"Hello, {user}!")


async def main():
    # Set the context variable within a context block
    user_var.set("John")

    await greet()  # Output: Hello, John!

    # Change the context variable within a nested context block
    async with user_var.replace("Alice"):
        await greet()  # Output: Hello, Alice!

    await greet()  # Output: Hello, John! (Restored to the previous value)


# Run the example
asyncio.run(main())

```

- 이 예제에서는 사용자 이름을 저장하기 위해 user라는 ContextVar를 정의한다.
- greet 함수는 get 메소드를 사용하여 user 변수의 값에 액세스한다.
- main 코루틴 내에서 user_var.set("John")을 사용하여 user 컨텍스트 변수를 "John"으로 설정한다. 그런 다음 user 변수의 현재 값을 검색하고 인쇄하는 greet 함수를 호출한다.
- 다음으로 async with user_var.replace("Alice")를 사용하여 중첩된 컨텍스트 블록을 만듭니다. 이 블록 내에서 user 변수는 일시적으로 "Alice" 값으로 대체된다. greet 함수를 다시 호출하면 "Hello, Alice!"가 출력된다.
- 중첩된 컨텍스트 블록이 끝나면 user 변수는 이전 값("John")으로 복원되고 greet를 호출하면 "Hello, John!"이 인쇄된다. 다시.
- ContextVar 클래스를 사용하면 전역 변수에 의존하거나 함수 또는 코루틴을 통해 인수를 명시적으로 전달하지 않고도 컨텍스트별 데이터를 저장하고 검색할 수 있습니다. Python에서 컨텍스트 종속 정보를 관리하는 편리한 방법을 제공한다.

---

## contextvars 및 uuid를 사용하여 FastAPI 요청을 격리하고 고유 식별자와 연결할 수 있습니다. 이는 FastAPI 애플리케이션 내에서 요청별 데이터 또는 상태를 추적하고 관리

```
from fastapi import FastAPI, Request
import contextvars
import uuid

# Create a context variable to store the request ID
request_id_var = contextvars.ContextVar("request_id")


def get_request_id() -> str:
    # Retrieve the current request ID from the context variable
    request_id = request_id_var.get()
    if request_id is None:
        # If no request ID exists, generate a new one
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)
    return request_id


app = FastAPI()


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    # Generate or retrieve the request ID and add it to the request headers
    request_id = get_request_id()
    request.headers["X-Request-ID"] = request_id

    # Set the request ID in the context variable for the duration of the request
    async with request_id_var.replace(request_id):
        response = await call_next(request)

    return response


@app.get("/")
async def root(request_id: str = None):
    # Retrieve the request ID from the context variable
    current_request_id = get_request_id()

    return {"message": "Hello, World!", "current_request_id": current_request_id, "provided_request_id": request_id}

```

- JSON 응답을 반환하는 단일 경로("/")로 FastAPI 애플리케이션을 정의한다. 미들웨어 기능인 add_request_id_header를 사용하여 들어오는 각 요청에 사용자 지정 헤더(X-Request-ID)를 추가한다. 이 헤더에는 고유한 요청 식별자가 포함된다.

- 미들웨어 내에서 get_request_id 함수를 호출하여 요청 ID를 검색하거나 생성한다. 요청 ID가 컨텍스트 변수에 이미 있으면 검색된다. 그렇지 않으면 새 UUID가 생성되어 컨텍스트 변수에 설정된다.

- get_request_id 함수는 request_id_var.get()을 사용하여 컨텍스트 변수에서 요청 ID를 검색한다. 요청 ID가 없으면 uuid.uuid4()를 사용하여 새 UUID를 생성하고 컨텍스트 변수에 설정한다.

- 마지막으로 루트 경로("/")에서 get_request_id를 사용하여 현재 요청 ID를 검색하고 제공된 요청 ID(있는 경우)와 함께 응답으로 반환한다.

- contextvars 및 uuid를 사용하면 각 요청에 연결된 고유 식별자가 있으므로 FastAPI 애플리케이션 전체에서 요청별 데이터 또는 상태를 격리하고 추적할 수 있다.

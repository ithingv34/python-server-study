import uuid

from fastapi import FastAPI
from loguru import logger
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware


_request_id = ContextVar("request_id", default=None)


def get_request_id():
    return _request_id.get()


class ContextualizeRequest(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        uuid = uuid.uuid4()  # `get_uuid()`는 사용자 정의 함수로 구현되어야 합니다.
        request_id = _request_id.set(uuid)  # set uuid to context variable
        with logger.contextualize(uuid=get_request_id()):
            try:
                response = await call_next(request)
            except Exception:
                logger.error("Request failed")
            finally:
                _request_id.reset()
                return response


app = FastAPI()

# 미들웨어 등록
app.add_middleware(ContextualizeRequest)


# 라우트 및 핸들러 등록
@app.get("/")
async def root():
    logger.info("Hello, World!")
    return {"message": "Hello, World!"}

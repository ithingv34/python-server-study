from fastapi import FastAPI

from server.db import init_db
from server.routes.book_review import router as ReviewRouter

app = FastAPI()

app.include_router(ReviewRouter, tags=['Book Reviews'], prefix='/reviews')

@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}
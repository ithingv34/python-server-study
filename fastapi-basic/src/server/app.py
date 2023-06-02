from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
def get_users(is_admin: bool, limit: int = 100):  # 추가: q
    return {"is_admin": is_admin, "limit": limit}  # 추가: q

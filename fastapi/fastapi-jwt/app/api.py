from fastapi import FastAPI, Body,  Depends
from fastapi.middleware.cors import CORSMiddleware

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT


posts = [
    {
        "id": 1,
        "title": "1번째 글",
        "content": "Fastapi"
    },
    {
        "id": 2,
        "title": "2번째 글",
        "content": "User Authentication Using JWT"
    }
]

users = []


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

@app.post('/user/singup', tags=['user'])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "wrong login detail"
    }


@app.get("/", tags=["root"])
async def home() -> dict:
    return {"message": "Server is running...."}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "message": posts }


@app.get("/posts/{id}", tags=["posts"])
async def get_post(id: int) -> dict:
    for post in posts:
        if post['id'] == id:
            return {
                "message": post
            }
    return { "message": "post not found" }


@app.post("/posts", 
          dependencies=[Depends(JWTBearer())],
          tags=['posts'])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "message": { "post added." }
    }


@app.put("/posts/{id}", tags=["posts"])
async def update_post(id: int, body: dict) -> dict:
    for post in posts:
        if post["id"] == id:
            post["item"] = body["item"]
            return {
                "message": f"post with id {id} has benn updated"
            }
    return {
        "message": f"post with id {id} not found"
    }


@app.delete("/posts/{id}", tags=["posts"])
async def delete_post(id: int) -> dict:
    for post in posts:
        if post["id"] == id:
            posts.remove(posts)
            return {
                "message": f"post with id {id} has been removed."
            }
    return {
        "message": f"post with id {id} not found."
    }
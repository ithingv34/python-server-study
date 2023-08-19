from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.models.book_review import BookReview


async def init_db():
    client = AsyncIOMotorClient(
        "mongodb://localhost:27017/"
    )

    database = client.bookreviews

    await init_beanie(database=database, document_models=[BookReview])
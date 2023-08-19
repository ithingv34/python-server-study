from datetime import datetime

from beanie import Document
from pydantic import BaseModel
from typing import Optional


class BookReview(Document):
    title: str
    rating: float
    review: str
    date: datetime = datetime.now()

    class Settings:
        name = "book_review"

    class Config:
        schema_extra = {
            "example": {
                "title": "Designing Machine Learning Systems",
                "rating": 4.9,
                "review": "Excellent book!",
                "date": datetime.now()
            }
        }


class UpdateBookReview(BaseModel):
    title: Optional[str]
    rating: Optional[float]
    review: Optional[str]
    date: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "title": "Designing Machine Learning Systems",
                "rating": 5.0,
                "review": "Excellent book!",
                "date": datetime.now()
            }
        }
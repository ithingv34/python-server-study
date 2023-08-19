from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from typing import List

from server.models.book_review import BookReview, UpdateBookReview


router = APIRouter()


@router.post("/", response_description="Review added to the database")
async def add_review(review: BookReview) -> dict:
    await review.create()
    return {"message": "Review added successfully"}


@router.get("/{id}", response_description="Review record retrieved")
async def get_review_record(id: PydanticObjectId) -> BookReview:
    review = await BookReview.get(id)
    return review


@router.get("/", response_description="Review records retrieved")
async def get_reviews() -> List[BookReview]:
    reviews = await BookReview.find_all().to_list()
    return reviews


@router.put("/{id}", response_description="Review record updated")
async def update_review_data(id: PydanticObjectId, req: UpdateBookReview) -> BookReview:
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}

    review = await BookReview.get(id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )

    await review.update(update_query)
    return review


@router.delete("/{id}", response_description="Review record deleted from the database")
async def delete_review_data(id: PydanticObjectId) -> dict:
    record = await BookReview.get(id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )

    await record.delete()
    return {
        "message": "Record deleted successfully"
    }
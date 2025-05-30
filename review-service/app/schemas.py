from pydantic import BaseModel

class ReviewCreate(BaseModel):
    book_id: int
    rating: int
    comment: str

class ReviewOut(ReviewCreate):
    id: int
    user_email: str

    class Config:
        orm_mode = True

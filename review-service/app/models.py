from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    user_email = Column(String, index=True)
    rating = Column(Integer)
    comment = Column(String)

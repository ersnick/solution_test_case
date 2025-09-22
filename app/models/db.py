from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FeedbackDB(Base):
    __tablename__ = "feedbacks"

    id = Column(String, primary_key=True, index=True)  # id отзыва WB
    nm_id = Column(Integer, index=True)
    created_date = Column(DateTime(timezone=True))
    rating = Column(Integer)
    full_text = Column(String)

from typing import List
from pydantic import BaseModel, computed_field
from datetime import datetime


class Product(BaseModel):
    root: int


class DetailResponse(BaseModel):
    products: List[Product]


class Feedback(BaseModel):
    id: str
    nmId: int
    createdDate: str
    productValuation: int
    pros: str
    text: str
    cons: str

    @computed_field
    @property
    def full_text(self) -> str:
        return (
            f"Достоинства: {self.pros or '-'}\n"
            f"Недостатки: {self.cons or '-'}\n"
            f"Комментарий: {self.text or '-'}"
        )

    def created_datetime(self) -> datetime:
        return datetime.fromisoformat(self.createdDate.replace("Z", "+00:00"))


class FeedbackResponse(BaseModel):
    feedbacks: List[Feedback]

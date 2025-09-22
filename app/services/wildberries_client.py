import aiohttp
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy import select

from app.models.schemas import DetailResponse, Feedback, FeedbackResponse
from app.models.db import FeedbackDB
from app.database import async_session
from app.logger import get_logger

logger = get_logger(__name__)


class WildberriesClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_root_by_nm(self, nm: str) -> int:
        url = (
            f"https://u-card.wb.ru/cards/v4/detail?"
            f"appType=1&curr=rub&dest=-1581744&spp=30&ab_testing=false&lang=ru&nm={nm}"
        )
        try:
            async with self.session.get(url) as response:
                data = await response.json()
                parsed = DetailResponse.model_validate(data)
                return parsed.products[0].root
        except Exception as e:
            logger.exception(f"Ошибка при получении root для nm={nm}: {e}")
            raise

    async def get_feedbacks(self, root: int) -> List[Feedback]:
        feed_url = f"https://feedbacks1.wb.ru/feedbacks/v1/{root}"
        try:
            async with self.session.get(feed_url) as response:
                data = await response.json()
                parsed = FeedbackResponse.model_validate(data)
                return parsed.feedbacks
        except Exception as e:
            logger.exception(f"Ошибка при получении отзывов root={root}: {e}")
            raise

    async def get_bad_feedbacks(
        self, nm: str, rating: int, days_ago: Optional[int] = None
    ) -> List[Feedback]:
        try:
            root = await self.get_root_by_nm(nm)
            feedbacks = await self.get_feedbacks(root)

            result = [
                fb for fb in feedbacks
                if fb.productValuation < rating and fb.nmId == int(nm)
            ]

            if days_ago:
                cutoff = datetime.now(timezone.utc) - timedelta(days=days_ago)
                result = [fb for fb in result if fb.created_datetime() >= cutoff]

            return result
        except Exception as e:
            logger.exception(f"Ошибка при фильтрации плохих отзывов nm={nm}: {e}")
            return []

    async def save_feedbacks(self, feedbacks: List[Feedback]):
        """Сохраняет отзывы в БД, исключая дубликаты"""
        try:
            async with async_session() as session:
                for fb in feedbacks:
                    exists = await session.execute(
                        select(FeedbackDB).where(FeedbackDB.id == fb.id)
                    )
                    if exists.scalars().first():
                        continue

                    new_feedback = FeedbackDB(
                        id=fb.id,
                        nm_id=fb.nmId,
                        created_date=fb.created_datetime(),
                        rating=fb.productValuation,
                        full_text=fb.full_text,
                    )
                    session.add(new_feedback)

                await session.commit()
        except Exception as e:
            logger.exception(f"Ошибка при сохранении отзывов в БД: {e}")
            raise

import asyncio
import sys
import aiohttp
import argparse

from app.services.wildberries_client import WildberriesClient
from app.database import init_db
from app.logger import get_logger

logger = get_logger(__name__)


async def run(nm: str, rating: int, days: int):
    try:
        async with aiohttp.ClientSession() as http_session:
            client = WildberriesClient(http_session)
            bad_feedbacks = await client.get_bad_feedbacks(nm, rating, days)
            logger.info(f"Найдено {len(bad_feedbacks)} плохих отзывов для nm={nm}")

            await client.save_feedbacks(bad_feedbacks)
            logger.info("Сохранение отзывов в БД завершено.")
    except Exception as e:
        logger.exception(f"Ошибка при обработке nm={nm}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Сбор плохих отзывов Wildberries")
    parser.add_argument("nm", type=str, help="Артикул товара")
    parser.add_argument(
        "--rating", type=int, default=3, help="Минимальный рейтинг (по умолчанию 3)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="Начало отсчета (дней) для отзывов (по умолчанию 3)",
    )
    return parser.parse_args()


async def main():
    try:
        args = parse_args()
        await init_db()
        await run(args.nm, args.rating, args.days)
    except Exception as e:
        logger.exception(f"Критическая ошибка в main: {e}")


if __name__ == "__main__":
    asyncio.run(main())

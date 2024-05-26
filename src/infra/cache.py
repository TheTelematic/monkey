from redis.asyncio import Redis

import config
from logger import logger

redis_queries = Redis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB_QUERIES, password=config.REDIS_PASSWORD
)
redis_translations = Redis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB_TRANSLATIONS, password=config.REDIS_PASSWORD
)


async def graceful_shutdown_redis():
    logger.info("Closing Redis connection...")
    await redis_queries.close()
    await redis_translations.close()

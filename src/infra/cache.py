from redis.asyncio import Redis

import config
from logger import logger

redis = Redis(host=config.REDIS_HOST, port=6379, db=0, password=config.REDIS_PASSWORD)


async def graceful_shutdown_redis():
    logger.info("Closing Redis connection...")
    await redis.close()

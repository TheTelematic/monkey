from redis.asyncio import Redis
from redis.commands.core import ResponseT
from redis.typing import KeyT

import config
from logger import logger


class PrefixedRedis(Redis):
    def __init__(self, *args, **kwargs):
        self.prefix_keys = kwargs.pop("prefix_keys", "")
        super().__init__(*args, **kwargs)

    async def set(
        self,
        name: KeyT,
        *args,
        **kwargs,
    ) -> ResponseT:
        return await super().set(f"{self.prefix_keys}:{name}", *args, **kwargs)

    async def get(
        self,
        name: KeyT,
    ) -> ResponseT:
        return await super().get(f"{self.prefix_keys}:{name}")


redis_queries = PrefixedRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD, prefix_keys="queries"
)
redis_translations = PrefixedRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD, prefix_keys="translations"
)


async def graceful_shutdown_redis():
    logger.info("Closing Redis connection...")
    try:
        await redis_queries.close()
        await redis_translations.close()
    except Exception as exc:
        logger.exception(f"Error closing Redis connection. {exc=}")

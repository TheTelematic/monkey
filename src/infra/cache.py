from hashlib import sha1

from redis.asyncio import Redis
from redis.commands.core import ResponseT
from redis.typing import KeyT

import config
from logger import logger


def hash_key(key: str) -> str:
    return sha1(key.encode()).hexdigest()


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

    async def exists(self, *names: KeyT) -> ResponseT:
        return await super().exists(*[f"{self.prefix_keys}:{name}" for name in names])


_redis_queries: PrefixedRedis | None = None
_redis_translations: PrefixedRedis | None = None

redis_translations = PrefixedRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD, prefix_keys="translations"
)


def get_redis_queries() -> PrefixedRedis:
    global _redis_queries
    if _redis_queries is None:
        logger.info("Creating a new Redis connection for queries...")
        _redis_queries = PrefixedRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            password=config.REDIS_PASSWORD,
            prefix_keys="queries",
            single_connection_client=True,
        )

    return _redis_queries


def get_redis_translations() -> PrefixedRedis:
    global _redis_translations
    if _redis_translations is None:
        logger.info("Creating a new Redis connection for translations...")
        _redis_translations = PrefixedRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            password=config.REDIS_PASSWORD,
            prefix_keys="translations",
            single_connection_client=True,
        )

    return _redis_translations


async def graceful_shutdown_redis():
    global _redis_queries, _redis_translations
    logger.info("Closing Redis connection...")
    try:
        if _redis_queries is not None:
            await _redis_queries.aclose()
        if _redis_translations is not None:
            await _redis_translations.aclose()
    except Exception as exc:
        logger.exception(f"Error closing Redis connection. {exc=}")

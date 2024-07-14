from hashlib import sha1

from redis import RedisError
from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.commands.core import ResponseT
from redis.typing import KeyT

import config
from logger import logger

__COMMON_KWARGS = dict(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0,
    password=config.REDIS_PASSWORD,
    single_connection_client=True,
    retry_on_timeout=True,
    retry_on_error=[RedisError],
    retry=Retry(backoff=ExponentialBackoff(), retries=3),
)


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


def get_redis_queries() -> PrefixedRedis:
    global _redis_queries
    if _redis_queries is None:
        logger.info("Creating a new Redis connection for queries...")
        _redis_queries = PrefixedRedis(
            prefix_keys="queries",
            **__COMMON_KWARGS,
        )

    return _redis_queries


def get_redis_translations() -> PrefixedRedis:
    global _redis_translations
    if _redis_translations is None:
        logger.info("Creating a new Redis connection for translations...")
        _redis_translations = PrefixedRedis(
            prefix_keys="translations",
            **__COMMON_KWARGS,
        )

    return _redis_translations


async def graceful_shutdown_redis():
    global _redis_queries, _redis_translations
    try:
        logger.info("Closing Redis connection for queries...")
        if _redis_queries is not None:
            await _redis_queries.aclose()
            logger.info("Closed Redis connection for queries...")
    except Exception as exc:
        logger.exception(f"Error closing Redis connection for queries. {exc=}")

    try:
        logger.info("Closing Redis connection for translations...")
        if _redis_translations is not None:
            await _redis_translations.aclose()
            logger.info("Closed Redis connection for translations...")
    except Exception as exc:
        logger.exception(f"Error closing Redis connection for translations. {exc=}")

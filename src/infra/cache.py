from hashlib import sha1

from redis.asyncio import Redis
from redis.commands.core import ResponseT
from redis.exceptions import ConnectionError as RedisConnectionError
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

    async def is_connected(self) -> bool:
        connection = self.connection
        if not connection:
            pool = self.connection_pool
            connection = pool.get_available_connection()
            try:
                await pool.ensure_connection(connection)
            except RedisConnectionError:
                return False

        return connection.is_connected


_redis_queries: PrefixedRedis | None = None
_redis_translations: PrefixedRedis | None = None

redis_translations = PrefixedRedis(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD, prefix_keys="translations"
)


async def get_redis_queries() -> PrefixedRedis:
    global _redis_queries
    if _redis_queries is None or not await _redis_queries.is_connected():
        logger.info("Creating a new Redis connection for queries...")
        _redis_queries = PrefixedRedis(
            host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD, prefix_keys="queries"
        )

    return _redis_queries


async def get_redis_translations() -> PrefixedRedis:
    global _redis_translations
    if _redis_translations is None or not await _redis_translations.is_connected():
        logger.info("Creating a new Redis connection for translations...")
        _redis_translations = PrefixedRedis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=0,
            password=config.REDIS_PASSWORD,
            prefix_keys="translations",
        )

    return _redis_translations


async def graceful_shutdown_redis():
    global _redis_queries, _redis_translations
    logger.info("Closing Redis connection...")
    try:
        if _redis_queries is not None and await _redis_queries.is_connected():
            await _redis_queries.aclose()
        if _redis_translations is not None and await _redis_translations.is_connected():
            await _redis_translations.aclose()
    except Exception as exc:
        logger.exception(f"Error closing Redis connection. {exc=}")

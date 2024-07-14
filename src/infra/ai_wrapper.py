import config
from infra.cache import get_redis_queries, hash_key, PrefixedRedis
from infra.ai.factory import AIEngineFactory, AIEngineTypes
from logger import logger
from metrics import Observer, monkey_ai_engine_invoke_duration_seconds, monkey_ai_engine_cache_hit_count


class AIWrapper:
    def __init__(self, ai_engine_type: AIEngineTypes):
        self.ai_engine_type = ai_engine_type
        self._engine = AIEngineFactory.get_ai_engine(ai_engine_type)

    @staticmethod
    async def _redis() -> PrefixedRedis:
        return await get_redis_queries()

    async def load_data(self):
        await self._engine.load_data()

    async def invoke(self, text: str, with_cache: bool = True) -> str:
        if not with_cache or not await self._cached(text) or not (result := await self._get_cache(text)):
            return await self._invoke_ai_engine(text, cache_response=with_cache)

        logger.debug(f"Using cache for {text=}")
        monkey_ai_engine_cache_hit_count.labels(self.ai_engine_type).inc()
        return result

    async def _invoke_ai_engine(self, text: str, cache_response: bool = False) -> str:
        logger.info("Invoking ai_engine...")
        with Observer(monkey_ai_engine_invoke_duration_seconds.labels(self.ai_engine_type)):
            result = await self._engine.invoke(text)
            logger.debug(f"ai_engine response: {result}")

        if cache_response:
            logger.debug(f"Caching response of {text=}")
            await self._set_cache(text, result)

        return result

    async def _cached(self, text: str) -> bool:
        key = self._get_key(text)
        redis = await self._redis()
        return await redis.exists(key) == 1

    async def _get_cache(self, text: str) -> str:
        key = self._get_key(text)
        redis = await self._redis()
        return self._decode_value(await redis.get(key))

    async def _set_cache(self, text: str, result: str) -> None:
        key = self._get_key(text)
        value = self._encode_value(result)
        redis = await self._redis()
        await redis.set(key, value, ex=config.CACHE_EXPIRATION_SECONDS)

    @staticmethod
    def _get_key(text: str) -> str:
        return hash_key(text)

    @classmethod
    def _encode_value(cls, value: str) -> bytes:
        return value.encode("utf-8")

    @classmethod
    def _decode_value(cls, value: bytes) -> str:
        return value.decode("utf-8")


ai_engine_chat = AIWrapper(AIEngineTypes.CHAT)
ai_engine_web_content_crawler = AIWrapper(AIEngineTypes.WEB_CONTENT_CRAWLER)

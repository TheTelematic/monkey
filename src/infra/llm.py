import config
from infra.cache import redis_queries
from infra.llms.factory import LLMFactory
from logger import logger
from metrics import Observer, monkey_llm_invoke_duration_seconds, monkey_llm_cache_hit_count


class LLM:
    def __init__(self):
        self._engine = LLMFactory.create_llm(config.LLM_ENGINE)

    async def invoke(self, text: str, with_cache: bool = True) -> str:
        if not with_cache or not await self._cached(text) or not (result := await self._get_cache(text)):
            return await self._invoke_llm(text, cache_response=with_cache)

        logger.debug(f"Using cache for {text=}")
        monkey_llm_cache_hit_count.inc()
        return result

    async def _invoke_llm(self, text: str, cache_response: bool = False) -> str:
        logger.info("Invoking LLM...")
        with Observer(monkey_llm_invoke_duration_seconds.labels(config.LLM_ENGINE)):
            result = await self._engine.invoke(text)
            logger.debug(f"LLM response: {result}")

        if cache_response:
            logger.debug(f"Caching response of {text=}")
            await self._set_cache(text, result)

        return result

    async def _cached(self, text: str) -> bool:
        key = self._get_key(text)
        return await redis_queries.exists(key) == 1

    async def _get_cache(self, text: str) -> str:
        key = self._get_key(text)
        return self._decode_value(await redis_queries.get(key))

    async def _set_cache(self, text: str, result: str) -> None:
        key = self._get_key(text)
        value = self._encode_value(result)
        await redis_queries.set(key, value, ex=config.CACHE_EXPIRATION_SECONDS)

    @staticmethod
    def _get_key(text: str) -> str:
        return text

    @classmethod
    def _encode_value(cls, value: str) -> bytes:
        return value.encode("utf-8")

    @classmethod
    def _decode_value(cls, value: bytes) -> str:
        return value.decode("utf-8")


llm = LLM()

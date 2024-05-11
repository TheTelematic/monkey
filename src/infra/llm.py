from langchain_community.llms import Ollama

import config
from infra.cache import redis
from logger import logger


class LLM:
    def __init__(self):
        self.llm = Ollama(base_url=config.LLM_URL, model="llama3")
        self.redis = redis

    async def invoke(self, text: str, with_cache: bool = True) -> str:
        if not with_cache or not await self._cached(text):
            return await self._invoke_llm(text, cache_response=with_cache)

        logger.debug(f"Using cache for {text=}")
        return await self._get_cache(text)

    async def _invoke_llm(self, text: str, cache_response: bool = False) -> str:
        logger.info("Invoking LLM...")
        result = await self.llm.ainvoke(text)
        logger.debug(f"LLM response: {result}")

        if cache_response:
            logger.debug(f"Caching response of {text=}")
            await self._set_cache(text, result)

        return result

    async def _cached(self, text: str) -> bool:
        return await self.redis.exists(text) == 1

    async def _get_cache(self, text: str) -> str:
        return await self.redis.get(text)

    async def _set_cache(self, text: str, result: str) -> None:
        await self.redis.set(text, result, ex=config.CACHE_EXPIRATION_SECONDS)


llm = LLM()

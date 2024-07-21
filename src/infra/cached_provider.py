import config
from infra.cache import get_redis_queries, hash_key, PrefixedRedis
from infra.providers.factory import ProvidersFactory, ProviderTypes
from logger import logger
from metrics import Observer, monkey_provider_invoke_duration_seconds, monkey_provider_cache_hit_count


class CachedProvider:
    def __init__(self, provider_type: ProviderTypes):
        self.provider_type = provider_type
        self._engine = ProvidersFactory.get_provider(provider_type)

    @staticmethod
    async def _redis() -> PrefixedRedis:
        return await get_redis_queries()

    async def load_data(self):
        await self._engine.load_data()

    async def invoke(self, text: str, with_cache: bool = True) -> str:
        if not with_cache or not await self._cached(text) or not (result := await self._get_cache(text)):
            return await self._invoke_provider(text, cache_response=with_cache)

        logger.debug(f"Using cache for {text=}")
        monkey_provider_cache_hit_count.labels(self.provider_type).inc()
        return result

    async def _invoke_provider(self, text: str, cache_response: bool = False) -> str:
        logger.info(f"Invoking provider {self.provider_type}...")
        with Observer(monkey_provider_invoke_duration_seconds.labels(self.provider_type)):
            result = await self._engine.invoke(text)
            logger.debug(f"provider response: {result}")

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


chat_provider: CachedProvider | None = None
google_images_search_provider: CachedProvider | None = None
web_content_crawler_provider: CachedProvider | None = None


def load_providers():
    global chat_provider, web_content_crawler_provider, google_images_search_provider

    if chat_provider is None:
        chat_provider = CachedProvider(ProviderTypes.CHAT)

    if google_images_search_provider is None:
        google_images_search_provider = CachedProvider(ProviderTypes.SEARCH_IMAGES)

    if web_content_crawler_provider is None:
        web_content_crawler_provider = CachedProvider(ProviderTypes.WEB_CONTENT_CRAWLER)

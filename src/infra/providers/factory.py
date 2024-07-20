from enum import Enum

from infra.providers.base import ProviderBase
from infra.providers.impl.google import GoogleImagesSearch
from infra.providers.impl.web_content_crawler import ApifyContentCrawler
from infra.providers.impl.chat import OpenAI


class ProviderTypes(Enum):
    CHAT = "chat"
    WEB_CONTENT_CRAWLER = "web_content_crawler"
    SEARCH_IMAGES = "search_images"


class ProvidersFactory:
    _engines = {
        ProviderTypes.CHAT: OpenAI,
        ProviderTypes.WEB_CONTENT_CRAWLER: ApifyContentCrawler,
        ProviderTypes.SEARCH_IMAGES: GoogleImagesSearch,
    }

    @classmethod
    def get_provider(cls, provider_type: ProviderTypes) -> ProviderBase:
        return cls._engines[provider_type]()

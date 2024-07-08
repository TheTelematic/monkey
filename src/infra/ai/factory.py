from enum import Enum

from infra.ai.base import AIEngineBase
from infra.ai.impl.web_content_crawler import ApifyContentCrawler
from infra.ai.impl.chat import OpenAI


class AIEngineTypes(Enum):
    CHAT = "chat"
    WEB_CONTENT_CRAWLER = "web_content_crawler"


class AIEngineFactory:
    _engines = {AIEngineTypes.CHAT: OpenAI, AIEngineTypes.WEB_CONTENT_CRAWLER: ApifyContentCrawler}

    @classmethod
    def get_ai_engine(cls, ai_engine_type: AIEngineTypes) -> AIEngineBase:
        return cls._engines[ai_engine_type]()

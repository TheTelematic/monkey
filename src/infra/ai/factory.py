from enum import Enum

from infra.ai.base import LLMBase
from infra.ai.impl.web_content_crawler import ApifyContentCrawler
from infra.ai.impl.chat import OpenAI


class LLMTypes(Enum):
    CHAT = "chat"
    WEB_CONTENT_CRAWLER = "web_content_crawler"


class LLMFactory:
    _engines = {LLMTypes.CHAT: OpenAI, LLMTypes.WEB_CONTENT_CRAWLER: ApifyContentCrawler}

    @classmethod
    def create_llm(cls, llm_type: LLMTypes) -> LLMBase:
        return cls._engines[llm_type]()

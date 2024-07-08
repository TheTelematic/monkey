from enum import Enum

from infra.llms.base import LLMBase
from infra.llms.impl.apify import ApifyContentCrawler
from infra.llms.impl.openai import OpenAI


class LLMTypes(Enum):
    CHAT = "chat"
    WEB_CONTENT_CRAWLER = "web_content_crawler"


class LLMFactory:
    _engines = {LLMTypes.CHAT: OpenAI, LLMTypes.WEB_CONTENT_CRAWLER: ApifyContentCrawler}

    @classmethod
    def create_llm(cls, llm_type: LLMTypes) -> LLMBase:
        return cls._engines[llm_type]()

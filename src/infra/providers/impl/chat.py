from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

import config
from infra.providers.base import ProviderBase
from logger import logger
from metrics import monkey_openai_token_usage_total_tokens


class OpenAI(ProviderBase):
    MODEL = "gpt-4o"

    def __init__(self):
        self._check_config()

        self.ai_engine = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model=self.MODEL)

    @staticmethod
    def _check_config():
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the config.")

    async def load_data(self):
        logger.warning("OpenAI does not require loading data.")

    async def invoke(self, text: str) -> str:
        result: AIMessage = await self.ai_engine.ainvoke(text)
        monkey_openai_token_usage_total_tokens.labels(self.MODEL).inc(
            result.response_metadata["token_usage"]["total_tokens"]
        )
        return result.content

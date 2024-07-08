from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

import config
from infra.ai.base import LLMBase
from metrics import monkey_openai_token_usage_total_tokens


class OpenAI(LLMBase):
    MODEL = "gpt-4o"

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the config.")

        self.llm = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model=self.MODEL)

    async def invoke(self, text: str) -> str:
        result: AIMessage = await self.llm.ainvoke(text)
        monkey_openai_token_usage_total_tokens.labels(self.MODEL).inc(
            result.response_metadata["token_usage"]["total_tokens"]
        )
        return result.content

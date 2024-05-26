from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

import config
from infra.llms.base import LLMBase


class OpenAI(LLMBase):
    MODEL = "gpt-4o"

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the config.")

        self.llm = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model=self.MODEL)

    async def invoke(self, text: str) -> str:
        result: AIMessage = await self.llm.ainvoke(text)
        return result.content

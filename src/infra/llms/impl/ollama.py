import config
from infra.llms.base import LLMBase
from langchain_community.llms import Ollama as _Ollama


class Ollama(LLMBase):
    MODEL = "llama3"

    def __init__(self):
        if not config.OLLAMA_URL:
            raise ValueError("OLLAMA_URL is not set in the config.")

        self.llm = _Ollama(base_url=config.OLLAMA_URL, model=self.MODEL)

    async def invoke(self, text: str) -> str:
        result = await self.llm.ainvoke(text)
        return result

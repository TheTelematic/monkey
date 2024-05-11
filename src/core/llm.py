from langchain_community.llms import Ollama

import config
from logger import logger


class LLM:
    def __init__(self):
        self.llm = Ollama(base_url=config.LLM_URL, model="llama3")

    async def invoke(self, text: str) -> str:
        logger.info("Invoking LLM...")
        result = await self.llm.ainvoke(text)
        logger.debug(f"LLM response: {result}")
        return result


llm = LLM()

from infra.llms.base import LLMBase
from infra.llms.impl.ollama import Ollama
from infra.llms.impl.openai import OpenAI


class LLMFactory:
    OLLAMA = "ollama"
    OPENAI = "openai"

    _engines = {OLLAMA: Ollama, OPENAI: OpenAI}

    @classmethod
    def create_llm(cls, llm_type: str) -> LLMBase:
        return cls._engines[llm_type.lower()]()

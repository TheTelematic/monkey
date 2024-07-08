from infra.llms.base import LLMBase
from infra.llms.impl.openai import OpenAI


class LLMFactory:
    OPENAI = "openai"

    _engines = {OPENAI: OpenAI}

    @classmethod
    def create_llm(cls, llm_type: str) -> LLMBase:
        return cls._engines[llm_type.lower()]()

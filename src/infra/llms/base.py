from abc import abstractmethod


class LLMBase:
    @staticmethod
    @abstractmethod
    async def invoke(text: str) -> str:
        raise NotImplementedError

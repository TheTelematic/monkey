from abc import abstractmethod


class LLMBase:
    @abstractmethod
    async def invoke(self, text: str) -> str:
        raise NotImplementedError

from abc import abstractmethod


class AIEngineBase:
    @abstractmethod
    async def invoke(self, text: str) -> str:
        raise NotImplementedError

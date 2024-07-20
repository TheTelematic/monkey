from abc import abstractmethod


class ProviderBase:
    @abstractmethod
    async def invoke(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def load_data(self):
        raise NotImplementedError

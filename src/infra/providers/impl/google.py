import httpx

import config
from api.constants import STATIC_PATH
from infra.providers.base import ProviderBase


class GoogleImagesSearch(ProviderBase):
    def __init__(self):
        self._check_config()

        self.api_key = config.GOOGLE_IMAGES_SEARCH_API_KEY
        self.cx = config.GOOGLE_IMAGES_SEARCH_CX

    @staticmethod
    def _check_config():
        if not config.GOOGLE_IMAGES_SEARCH_API_KEY:
            raise ValueError("GOOGLE_IMAGES_SEARCH_API_KEY is not set in the config.")

        if not config.GOOGLE_IMAGES_SEARCH_CX:
            raise ValueError("GOOGLE_IMAGES_SEARCH_CX is not set in the config.")

    async def load_data(self):
        pass

    async def invoke(self, query: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "key": self.api_key,
                    "cx": self.cx,
                    "q": query,
                    "searchType": "image",
                },
            )
            try:
                response.raise_for_status()
                data = response.json()
                return data["items"][0]["link"]
            except httpx.HTTPStatusError:
                return f"{STATIC_PATH}/images/sample-phone.png"

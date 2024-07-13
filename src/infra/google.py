import httpx

import config


class GoogleImagesSearch:
    def __init__(self):
        self.api_key = config.GOOGLE_IMAGES_SEARCH_API_KEY
        self.cx = config.GOOGLE_IMAGES_SEARCH_CX

    async def get_image_link(self, query: str) -> str:
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
            response.raise_for_status()
            data = response.json()
            return data["items"][0]["link"]


google_images_search = GoogleImagesSearch()

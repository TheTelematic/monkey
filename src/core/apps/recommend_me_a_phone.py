import json

from infra.llm import llm_web_content_crawler
from logger import logger

_PROMPT = (
    "Can you tell me the top 5 of best phones please? "
    "Please provide name, price and some details about each phone. "
    "I give you an example of the format of the output, please respect and respond using it:"
    '{"phones": [{"name": "Samsung Galaxy S21", "price": "$799", '
    '"specifications": ["It has a 9 hours battery."], ["It has 6 inches display."]}]}'
)


async def get_phones_recommendations() -> dict:
    response = await llm_web_content_crawler.invoke(_PROMPT)
    if response.startswith("```json"):
        response = response.replace("```json", "").replace("```", "")

    logger.info(f"Response from Apify: {response}")
    return json.loads(response)

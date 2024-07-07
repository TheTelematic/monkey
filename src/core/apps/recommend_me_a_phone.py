import json

from infra.apify import apify

_PROMPT = (
    "Can you tell me the top 5 of best phones please? "
    "Please provide name, price and some details about each phone. "
    "I give you an example of the format of the output, please respect and respond using it:"
    '{"phones": [{"name": "Samsung Galaxy S21", "price": "$799", '
    '"specifications": ["It has a 9 hours battery."], ["It has 6 inches display."]}]}'
)


async def get_phones_recommendations() -> dict:
    return json.loads(await apify.invoke(_PROMPT))
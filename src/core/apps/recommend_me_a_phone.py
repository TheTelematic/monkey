import json

from dtos.recommend_me_a_phone import PhoneRecommendation
from infra.ai_wrapper import ai_engine_web_content_crawler
from infra.google import google_images_search
from logger import logger

_PROMPT = """
Can you make me the top of best phones please? 
Please provide name, price and some details about each phone. 
I give you an example of the format of the output, please respect and respond using it, avoid any other comment 
and respond with the requested information. The first character of the output must be '{' and the last one '}'.

EXAMPLE OF THE FORMAT:
{"phones": [{"name": "Phone Name", "price": "Phone Price", "specifications": ["Specification 1.", "Specification 2."]}]}

EXAMPLE OF THE OUTPUT:
{"phones": [{"name": "iPhone 13", "price": "$799", "specifications": ["A15 Bionic chip", "Super Retina XDR display"]}]}
"""


async def get_phone_recommendation() -> PhoneRecommendation:
    response = await ai_engine_web_content_crawler.invoke(_PROMPT)
    logger.info(f"Response from ai_engine_web_content_crawler: {response}")
    information = json.loads(response)
    first_phone = information["phones"][0]
    first_phone["picture_link"] = await google_images_search.get_image_link(first_phone["name"])
    return PhoneRecommendation(**first_phone)


async def _inject_phone_pictures(information: dict) -> dict:
    for phone in information["phones"]:
        phone["picture_link"] = await google_images_search.get_image_link(phone["name"])

    return information

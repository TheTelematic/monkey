import json

import config
from core.ai import get_ai_response
from dtos.recommend_me_a_phone import PhoneRecommendation, PhoneRecommendationWithJustification
from infra.cached_provider import web_content_crawler_provider, google_images_search
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

_PROMPT_WITH_FEEDBACK = """
Hello, given the following JSON information related to the best phones:
##### START JSON Information #####
{information}
##### END JSON Information #####

And the user feedback:
##### START User Feedback #####
{user_feedback}
##### END User Feedback #####

Previously, the chosen phone for the user was "{previous_phone_name}".
Could you please choose the best phone for the user based on the information provided?
Please respect the User Feedback section above to make the decision. 
Also, please start your response with the name of the phone, next to the character ':' and the explanation of your decision.
"""


async def get_phone_recommendation(
    current_phone_info: dict | None = None, user_feedback: str | None = None
) -> PhoneRecommendation:
    response = await web_content_crawler_provider.invoke(_PROMPT)
    logger.info(f"Response from ai_engine_web_content_crawler: {response}")
    information = json.loads(response)
    first_phone = information["phones"][0]
    if not user_feedback:
        first_phone["picture_link"] = await google_images_search.invoke(first_phone["name"])
        return PhoneRecommendation(**first_phone)
    else:
        if not current_phone_info:
            current_phone_info = first_phone

        prompt = _PROMPT_WITH_FEEDBACK.format(
            information=information, user_feedback=user_feedback, previous_phone_name=current_phone_info["name"]
        )
        logger.debug(f"Prompt for AI: {prompt}")
        response = await get_ai_response(prompt)
        logger.debug(f"Response from AI given the feedback '{user_feedback}': {response}")
        phone_name, justification = response.split(":")
        phone_info = next((phone for phone in information["phones"] if phone["name"] == phone_name), None)
        if phone_info and phone_info["name"] != first_phone["name"]:
            phone_info["picture_link"] = await google_images_search.invoke(phone_info["name"])
            return PhoneRecommendationWithJustification(
                name=phone_info["name"],
                price=phone_info["price"],
                specifications=phone_info["specifications"],
                picture_link=phone_info["picture_link"],
                justification=justification,
            )
        else:
            return PhoneRecommendationWithJustification(
                name=first_phone["name"],
                price=first_phone["price"],
                specifications=first_phone["specifications"],
                picture_link=await google_images_search.invoke(first_phone["name"]),
                justification=f"I'm sorry, I couldn't find the phone you requested. My information is based on {config.APIFY_CONTENT_CRAWLER_URL}.",
            )

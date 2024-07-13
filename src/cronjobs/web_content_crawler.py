import asyncio

from infra.ai_wrapper import ai_engine_web_content_crawler
from logger import logger


async def _crawl_web_content():
    logger.info("Crawling web content...")
    await ai_engine_web_content_crawler.load_data()
    logger.info("Web content crawled successfully.")


def run_web_content_crawler():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_crawl_web_content())
    loop.close()

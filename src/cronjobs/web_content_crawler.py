import asyncio

from infra.cached_provider import web_content_crawler_provider
from logger import logger


async def _crawl_web_content():
    logger.info("Crawling web content...")
    await web_content_crawler_provider.load_data()
    logger.info("Web content crawled successfully.")


def run_web_content_crawler():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_crawl_web_content())
    loop.close()

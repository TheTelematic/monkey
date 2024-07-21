import asyncio
import types
from typing import Coroutine

from core.probeness import check_dependencies, graceful_shutdown
from cronjobs.web_content_crawler import _crawl_web_content

cronjobs = types.SimpleNamespace()
CRONJOB_WEB_CONTENT_CRAWLER = "web_content_crawler"
cronjobs.CRONJOB_WEB_CONTENT_CRAWLER = CRONJOB_WEB_CONTENT_CRAWLER

_routes = {cronjobs.CRONJOB_WEB_CONTENT_CRAWLER: _crawl_web_content}


async def _run_cronjob(cronjob_coroutine: Coroutine):
    await check_dependencies()
    await cronjob_coroutine
    await graceful_shutdown()


def run_cronjob(cronjob: cronjobs) -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_routes[cronjob]())
    loop.close()

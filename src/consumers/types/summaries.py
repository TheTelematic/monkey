from core.summaries.summary import get_summary
from dtos.summaries import Summary
from logger import logger


async def make_summary(summary: Summary) -> None:
    logger.debug(f"Making summary of {summary=}")

    await get_summary(summary["text"], summary["language"])

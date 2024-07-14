from infra.broker import get_publisher_connection, graceful_shutdown_publisher
from infra.cache import get_redis_queries, get_redis_translations, graceful_shutdown_redis
from logger import logger


async def check_dependencies():
    try:
        redis_queries = get_redis_queries()
        await redis_queries.ping()

        redis_translations = get_redis_translations()
        await redis_translations.ping()

        connection = await get_publisher_connection()
        channel = await connection.channel()
        await channel.close()
    except Exception as exc:
        logger.exception(f"Error checking dependencies. {exc}")
        raise exc


async def graceful_shutdown():
    await graceful_shutdown_redis()
    await graceful_shutdown_publisher()

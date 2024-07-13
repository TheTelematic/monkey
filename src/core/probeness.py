from infra.broker import get_publisher_connection
from infra.cache import get_redis_queries, get_redis_translations


async def check_dependencies():
    redis_queries = await get_redis_queries()
    await redis_queries.ping()

    redis_translations = await get_redis_translations()
    await redis_translations.ping()

    connection = await get_publisher_connection()
    channel = await connection.channel()
    await channel.close()

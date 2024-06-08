from infra.broker import get_publisher_connection
from infra.cache import redis_queries, redis_translations


async def check_dependencies():
    await redis_queries.ping()
    await redis_translations.ping()

    connection = await get_publisher_connection()
    channel = await connection.channel()
    await channel.close()

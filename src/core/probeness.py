from infra.broker import get_publisher_connection
from infra.cache import get_redis_queries, get_redis_translations


async def check_dependencies():
    await (await get_redis_queries()).ping()
    await (await get_redis_translations()).ping()

    connection = await get_publisher_connection()
    channel = await connection.channel()
    await channel.close()

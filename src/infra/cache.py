from redis.asyncio import Redis

import config

redis = Redis(host=config.REDIS_HOST, port=6379, db=0, password=config.REDIS_PASSWORD)

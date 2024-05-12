import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)

OLLAMA_URL = os.getenv("OLLAMA_URL")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
CACHE_EXPIRATION_SECONDS = int(os.getenv("CACHE_EXPIRATION_SECONDS", 300))

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
assert RABBITMQ_URL, "RABBITMQ_URL environment variable is required"
RABBITMQ_PREFETCH_COUNT = int(os.getenv("RABBITMQ_PREFETCH_COUNT", 10))
RABBITMQ_QUEUE_TRANSLATIONS = os.getenv("RABBITMQ_QUEUE_TRANSLATIONS", "monkey.translations")

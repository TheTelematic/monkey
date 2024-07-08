import os

# Service configuration
APP_NAME = "monkey"
VERSION = os.getenv("VERSION")
DOMAIN_HOST = os.getenv("DOMAIN_HOST")

# API
POD_IP = os.getenv("POD_IP")
API_GRACEFUL_SHUTDOWN_TIMEOUT = int(os.getenv("API_GRACEFUL_SHUTDOWN_TIMEOUT", 30))
SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)
WS_PING_INTERVAL = int(os.getenv("WS_PING_INTERVAL", 60))
WS_PING_TIMEOUT = int(os.getenv("WS_PING_TIMEOUT", 60))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# LLM
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_CONTENT_CRAWLER_URL = os.getenv("APIFY_CONTENT_CRAWLER_URL")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Cache
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB_QUERIES = int(os.getenv("REDIS_DB_QUERIES", 0))
REDIS_DB_TRANSLATIONS = int(os.getenv("REDIS_DB_TRANSLATIONS", 1))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
CACHE_EXPIRATION_SECONDS = int(os.getenv("CACHE_EXPIRATION_SECONDS", 300))

# RabbitMQ
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_PREFETCH_COUNT = int(os.getenv("RABBITMQ_PREFETCH_COUNT", 10))
RABBITMQ_QUEUE_TRANSLATIONS = os.getenv("RABBITMQ_QUEUE_TRANSLATIONS", "monkey.translations")
RABBITMQ_QUEUE_SUMMARIES = os.getenv("RABBITMQ_QUEUE_SUMMARIES", "monkey.summaries")

# Consumers
LIVENESS_CONSUMERS_FILE = os.getenv("LIVENESS_CONSUMERS_FILE")
LIVENESS_CONSUMERS_SLEEP_TIME = int(os.getenv("LIVENESS_CONSUMERS_SLEEP_TIME", 5))

READINESS_CONSUMERS_FILE = os.getenv("READINESS_CONSUMERS_FILE")
READINESS_CONSUMERS_SLEEP_TIME = int(os.getenv("READINESS_CONSUMERS_SLEEP_TIME", 5))

# Prometheus
PROMETHEUS_INTERVAL = int(os.getenv("PROMETHEUS_INTERVAL", 5))

import os

SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)

LLM_URL = os.getenv("LLM_URL")

assert LLM_URL, "LLM_URL environment variable is required"

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

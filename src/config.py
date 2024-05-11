import os

SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)

LLM_URL = os.getenv("LLM_URL")

assert LLM_URL, "LLM_URL environment variable is required"

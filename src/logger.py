import logging

import config

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL.upper())
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - "
    "Process:%(process)d - Thread:%(thread)d - Task:%(taskName)s - %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Logger configured.")

import sys

import uvicorn

import config
from api.app import app
from consumers.main import run_consumer
from consumers.routes import consumers

if __name__ == "__main__":
    arg = sys.argv[1]
    match arg:
        case "api":
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=config.SERVICE_PORT,
                access_log=True,
                timeout_graceful_shutdown=config.API_GRACEFUL_SHUTDOWN_TIMEOUT,
                lifespan="on",
            )
        case "consumer_translations":
            run_consumer(consumers.TRANSLATIONS)
        case _:
            raise ValueError("Invalid argument. Use 'api' or 'consumer_translations'.")

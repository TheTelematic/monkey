import sys

import uvicorn

import config
from api.app import app
from consumers.workers import run_consumer, consumers

if __name__ == "__main__":
    arg = sys.argv[1]
    match arg:
        case "api":
            uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT, access_log=True)
        case "consumer_translations":
            run_consumer(consumers.TRANSLATIONS)
        case _:
            raise ValueError("Invalid argument. Use 'api' or 'consumer_translations'.")

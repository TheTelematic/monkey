import sys

import uvicorn

import config
from api.app import app
from logger import logger


if __name__ == "__main__":
    arg = sys.argv[1]
    match arg:
        case "api":
            uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT, access_log=True)
            logger.info("Service started at port 8000.")
        case _:
            raise ValueError("Invalid argument. Use 'api' to start the service.")

import os
import sys

import uvicorn

import config


if os.getenv("DEBUG"):
    import subprocess

    subprocess.run(["pip", "install", os.getenv("DEBUG_PYDEVD_PYCHARM")])
    import pydevd_pycharm

    pydevd_pycharm.settrace(
        os.getenv("DEBUG_HOST"),
        port=int(os.getenv("DEBUG_PORT")),
        stdoutToServer=True,
        stderrToServer=True,
        suspend=False,
    )


if __name__ == "__main__":
    arg = sys.argv[1]
    match arg:
        case "api":
            from api.app import app

            uvicorn.run(
                app,
                host="0.0.0.0",
                port=config.SERVICE_PORT,
                access_log=True,
                timeout_graceful_shutdown=config.API_GRACEFUL_SHUTDOWN_TIMEOUT,
                lifespan="on",
                ws_ping_interval=config.WS_PING_INTERVAL,
                ws_ping_timeout=config.WS_PING_TIMEOUT,
            )
        case "consumer":
            from consumers.main import run_consumer

            run_consumer(sys.argv[2])
        case "cronjobs":
            from cronjobs.main import run_cronjob

            run_cronjob(sys.argv[2])
        case _:
            raise ValueError("Invalid argument.")

import sys

import uvicorn

import config


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
        case _:
            from consumers.main import run_consumer
            from consumers.routes import consumers

            match arg:
                case "consumer_translations":
                    run_consumer(consumers.TRANSLATIONS)
                case "consumer_summaries":
                    run_consumer(consumers.SUMMARIES)
                case "cronjobs":
                    match sys.argv[2]:
                        case "web_content_crawler":
                            from cronjobs.web_content_crawler import run_web_content_crawler

                            run_web_content_crawler()
                case _:
                    raise ValueError("Invalid argument.")

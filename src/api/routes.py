from fastapi import APIRouter
from .ai.hello import router as ai_hello_router  # noqa: F401 # pylint: disable=unused-import


probes_router = APIRouter()


@probes_router.get("/readiness")
def readiness():
    return {"status": "ok"}


@probes_router.get("/liveness")
def liveness():
    return {"status": "ok"}

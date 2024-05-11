from fastapi import APIRouter

from infra.cache import redis

router = APIRouter()


@router.get("/readiness")
async def readiness():
    await redis.ping()
    return {"status": "ok"}


@router.get("/liveness")
def liveness():
    return {"status": "ok"}

from fastapi import APIRouter

from infra.cache import redis_queries, redis_translations

router = APIRouter()


@router.get("/readiness")
async def readiness():
    await redis_queries.ping()
    await redis_translations.ping()
    return {"status": "ok"}


@router.get("/liveness")
def liveness():
    return {"status": "ok"}

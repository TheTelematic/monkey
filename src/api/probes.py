from fastapi import APIRouter

from core.probeness import check_dependencies

router = APIRouter()


@router.get("/readiness")
async def readiness():
    await check_dependencies()
    return {"status": "ok"}


@router.api_route("/liveness", methods=["GET", "HEAD"])
async def liveness():
    return {"status": "ok"}

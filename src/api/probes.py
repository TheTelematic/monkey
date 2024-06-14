from fastapi import APIRouter

from core.probeness import check_dependencies

router = APIRouter()


@router.get("/readiness")
async def readiness():
    await check_dependencies()
    return {"status": "ok"}


@router.get("/liveness")
def liveness():
    return {"status": "ok"}


@router.head("/liveness")
def liveness():
    return {"status": "ok"}

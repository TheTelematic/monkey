from fastapi import APIRouter

router = APIRouter()


@router.get("/readiness")
def readiness():
    return {"status": "ok"}


@router.get("/liveness")
def liveness():
    return {"status": "ok"}

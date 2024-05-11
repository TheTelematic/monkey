from fastapi import APIRouter

from core.hello import hello as _hello

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    return {"message": await _hello()}

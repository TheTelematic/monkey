from fastapi import APIRouter

router = APIRouter(prefix="/hello")


@router.get("")
async def hello():
    return {"message": "Hello, World!"}

from fastapi import APIRouter
from pydantic import BaseModel

from core.summary import get_summary

router = APIRouter(prefix="/summary")


class Body(BaseModel):
    text: str


@router.post("")
async def make_summary(body: Body):
    return {"message": await get_summary(body.text)}

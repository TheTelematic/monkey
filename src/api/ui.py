from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import config

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/sandbox", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(request=request, name="sandbox.html", context={"app_name": config.APP_NAME})

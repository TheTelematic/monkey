from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

import config
from api.constants import STATIC_PATH

router = APIRouter()

templates = Jinja2Templates(directory="templates")
templates.env.globals["STATIC_PATH"] = STATIC_PATH
templates.env.globals["APP_NAME"] = config.APP_NAME
templates.env.globals["VERSION"] = config.VERSION
templates.env.globals["BUILD_TIMESTAMP"] = config.BUILD_TIMESTAMP


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/images/monkey-favicon.png")


@router.get("/sandbox", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(request=request, name="sandbox.html", context={"app_name": config.APP_NAME})


@router.get("/", response_class=HTMLResponse)
async def summary_and_translate(request: Request):
    return templates.TemplateResponse(
        request=request, name="summary_and_translate.html", context={"app_name": config.APP_NAME}
    )


@router.get("/recommend-me-a-phone", response_class=HTMLResponse)
async def recommend_me_a_phone(request: Request):
    return templates.TemplateResponse(
        request=request, name="recommend_me_a_phone.html", context={"app_name": config.APP_NAME}
    )

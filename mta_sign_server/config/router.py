import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(
    tags=["config"],
)

logger = logging.getLogger("config_router")


@router.get("/api/config")
def get_all():
    return JSONResponse({"config": "goes here"})

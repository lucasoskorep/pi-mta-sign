import json
import logging
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mta_sign_server.router import router as default_router
from mta_sign_server.mta.router import router as mta_router
from mta_sign_server.config.router import router as config_router

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(default_router)
app.include_router(mta_router)
app.include_router(config_router)

logger = logging.getLogger("main")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

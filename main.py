import logging
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from mta_sign_server.router import router as default_router
from mta_sign_server.mta.router import router as mta_router
from mta_sign_server.config.router import router as config_router

load_dotenv()

# Setup Swagger documentation
show_swagger = os.getenv("SHOW_SWAGGER", "false").lower() in ("true", "1", "yes")
swagger_config = {
    "docs_url": "/swagger" if show_swagger else None,
    "redoc_url": None,
    "openapi_url": "/openapi.json" if show_swagger else None,
}

app = FastAPI(**swagger_config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(default_router)
app.include_router(mta_router)
app.include_router(config_router)

logger = logging.getLogger("main")

# Serve static files from the Next.js build output
# In production, the 'static' directory contains the built frontend
# Set FRONTEND_ENABLE=false to disable serving static files
frontend_enabled = os.getenv("FRONTEND_ENABLE", "true").lower() not in ("false", "0", "no")
static_dir = Path(__file__).parent / "static"
if frontend_enabled and static_dir.exists():
    # Serve Next.js static assets (_next directory)
    next_static = static_dir / "_next"
    if next_static.exists():
        app.mount("/_next", StaticFiles(directory=str(next_static)), name="next-static")

    # Serve other static files (images, etc.)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    async def serve_index():
        """Serve the main index.html for the SPA"""
        return FileResponse(static_dir / "index.html")

    @app.get("/{path:path}")
    async def serve_spa(path: str):
        """Serve static files or fall back to index.html for SPA routing"""
        # Exclude API and documentation routes from SPA fallback
        if path.startswith(("api/", "swagger", "openapi", "redoc", "docs")):
            return {"error": "Not found"}

        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # Fall back to index.html for client-side routing
        return FileResponse(static_dir / "index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

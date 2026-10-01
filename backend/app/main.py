"""
Main application factory.

Creates and configures the FastAPI application:

  - Lifespan: connect MongoDB, ensure indexes, seed data, close on shutdown.
  - Middleware: CORS + request logging.
  - Exception handlers: consistent JSON error bodies.
  - Routers: /auth, /users, /admin, /diseases, /uploads, /predictions, /feedback.
  - Static serving of uploaded files.
  - Health check endpoint.

Run with:
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import close_db, ensure_indexes, ping_db
from app.middleware.error_handler import register_exception_handlers
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routes import (
    admin_routes,
    detect_routes,
    disease_routes,
    feedback_routes,
    prediction_routes,
    upload_routes,
    user_routes,
)
from app.auth import router as auth_router
from app.seed import seed_database
from app.utils.logger import setup_logging

settings = get_settings()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle hooks."""
    # --- Startup ---
    await ping_db()
    await ensure_indexes()
    await seed_database()
    yield
    # --- Shutdown ---
    await close_db()


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description=(
            "REST API for the Online Plant Disease Detection Portal. "
            "Connects React frontend to MongoDB."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    # --- Error handling ---
    register_exception_handlers(app)

    # --- Routers ---
    app.include_router(auth_router.router, prefix="/api")
    app.include_router(user_routes.router, prefix="/api")
    app.include_router(admin_routes.router, prefix="/api")
    app.include_router(disease_routes.router, prefix="/api")
    app.include_router(detect_routes.router, prefix="/api")
    app.include_router(upload_routes.router, prefix="/api")
    app.include_router(prediction_routes.router, prefix="/api")
    app.include_router(feedback_routes.router, prefix="/api")

    # --- Static files (uploaded images) ---
    from pathlib import Path

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

    # --- Health check ---
    @app.get("/", tags=["Health"], summary="Root", include_in_schema=False)
    async def root():
        return {
            "app": settings.app_name,
            "status": "ok",
            "docs": "/docs",
        }

    @app.get("/health", tags=["Health"], summary="Health check")
    async def health():
        """Simple liveness endpoint used by orchestrators/monitoring."""
        return {"status": "healthy", "database": "connected"}

    return app


# Module-level instance so `uvicorn app.main:app` works out of the box.
app = create_app()

"""
Global error handling.

Registers exception handlers so every error returns a consistent JSON body:

    {"detail": "<message>"}

Includes handlers for validation errors (422), HTTP errors, and unhandled
exceptions (500) with full server-side logging.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all exception handlers to the FastAPI app."""

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        """Return a readable 422 body listing the offending fields."""
        errors = []
        for err in exc.errors():
            loc = ".".join(str(p) for p in err.get("loc", []) if p != "body")
            errors.append({"field": loc, "message": err.get("msg", "Invalid value")})
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Validation error", "errors": errors},
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        """Log unexpected errors and return a generic 500."""
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    # HTTPException is handled by FastAPI by default, but we customise the shape.
    from fastapi import HTTPException
    from fastapi.exception_handlers import http_exception_handler

    @app.exception_handler(HTTPException)
    async def http_handler(request: Request, exc: HTTPException):
        return await http_exception_handler(request, exc)

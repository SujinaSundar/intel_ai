import logging

from app.exceptions.custom_exceptions import AppException
from app.exceptions.error_codes import ErrorCode
from app.exceptions.error_response import ErrorDetail, ErrorResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    """
    Register global exception handlers.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        logger.warning(
            f"{request.method} {request.url.path} -> {exc.error_code}: {exc.message}"
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code=exc.error_code,
                message=exc.message,
            )
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.warning(
            f"Validation Error: {exc.errors()}"
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCode.VALIDATION_ERROR,
                message="Validation failed.",
            )
        )

        return JSONResponse(
            status_code=422,
            content=response.model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        logger.warning(
            f"HTTP Exception: {exc.detail}"
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCode.INVALID_REQUEST,
                message=str(exc.detail),
            )
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(),
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ):
        logger.exception(exc)

        response = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCode.DATABASE_ERROR,
                message="Database operation failed.",
            )
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(exc)

        response = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred.",
            )
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump(),
        )
from fastapi import Request
from fastapi.responses import JSONResponse
from app.common.exceptions import CustomException
from app.common.logger import AppLogger


class ExceptionHandler:
    logger = AppLogger()

    @classmethod
    async def handle(cls, request: Request, exc: CustomException) -> JSONResponse:
        cls.logger.error(f"Exception occurred: {exc.message} | Path: {request.url}")

        return JSONResponse(
            status_code=exc.code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "path": str(request.url),
            },
        )

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = time.time() - start_time

        method_emoji = "📝" if request.method == "POST" else "📖"
        status_emoji = "✅" if 200 <= response.status_code < 300 else "⚠️"
        time_emoji = "⏱️"

        message = (
            f"{method_emoji} {request.client.host}:{request.client.port} "
            f"- {request.method} {request.url.path} - {status_emoji} {response.status_code} "
            f"{time_emoji} Completed in {processing_time:.3f}s"
        )

        print(message)
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "bookly-api-dc03.onrender.com",
            "0.0.0.0",
        ],
    )

    print("✨ Middleware registered: CORS + TrustedHost + Custom Logging ✅")

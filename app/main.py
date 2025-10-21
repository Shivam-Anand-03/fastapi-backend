from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import DatabaseConnect
from app.common.handlers.exception_handler import CustomException, ExceptionHandler
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.router import root_router
from app.common.services.redis_service import RedisClient
from .core.middleware.loggin import register_middleware
from fastapi.middleware.cors import CORSMiddleware

redis_client = RedisClient(password="shivam2003")


@asynccontextmanager
async def life_span(app: FastAPI):
    await DatabaseConnect.test_connection()
    await redis_client.connect()

    try:
        yield
    finally:
        await redis_client.close()
        print("🔒 Closed Redis connection")


class App:
    def __init__(self):
        self.app = FastAPI(lifespan=life_span)
        register_middleware(self.app)
        self.app.add_exception_handler(CustomException, ExceptionHandler.handle)
        self.app.include_router(root_router)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=[
                "localhost",
                "127.0.0.1",
                "bookly-api-dc03.onrender.com",
                "0.0.0.0",
            ],
        )

        @self.app.get("/")
        async def root():
            return {"message": "Hello from OOP FastAPI with DB and Redis!"}

    def get_app(self) -> FastAPI:
        return self.app


app_instance = App()
app = app_instance.get_app()

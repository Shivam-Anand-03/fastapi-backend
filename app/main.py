from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import DatabaseConnect  # Your DB connection class
from app.common.handlers.exception_handler import CustomException, ExceptionHandler
from app.core.router import root_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("🔌 Connecting to database...")
    await DatabaseConnect.init_db()
    try:
        yield
    finally:
        print("🔒 Closing database connection...")


class App:
    def __init__(self):
        self.app = FastAPI(lifespan=life_span)
        self.app.add_exception_handler(CustomException, ExceptionHandler.handle)
        self.app.include_router(root_router)

        @self.app.get("/")
        async def root():
            return {"message": "Hello from OOP FastAPI with DB!"}

    def get_app(self) -> FastAPI:
        return self.app


app_instance = App()
app = app_instance.get_app()

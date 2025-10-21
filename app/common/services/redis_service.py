from redis.asyncio import Redis
from typing import Optional, Any


class RedisClient:
    _instance: Optional["RedisClient"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        db: int = 0,
    ):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self._redis: Optional[Redis] = None
        self._initialized = True

    async def connect(self):
        if self._redis is None:
            self._redis = Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True,
            )
            await self._redis.ping()
            print("✅ Connected to Redis")

    async def close(self):
        if self._redis:
            await self._redis.close()
            self._redis = None

    @property
    def client(self) -> Redis:
        if not self._redis:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._redis

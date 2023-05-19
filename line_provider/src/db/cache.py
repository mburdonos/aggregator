import aioredis


class AsyncRedisStorage:
    async def startup(self, *args, **kwargs):
        """Redis initialization method"""
        self._redis = await aioredis.from_url(*args, **kwargs)

    async def shutdown(self):
        """Redis connection termination method"""
        self._redis.close()
        await self._redis.wait_closed()

    async def get(self, key: str) -> str:
        """Method for getting data from Redis"""
        return await self._redis.get(key)

    async def set(self, key: str, value: str, expire: int):
        """Data persistence method in Redis"""
        await self._redis.set(key, value, expire=expire)


redis: AsyncRedisStorage = AsyncRedisStorage()


async def get_redis() -> AsyncRedisStorage | None:
    """Function required for dependency injection"""
    return redis
from typing import Optional
from hashlib import md5
from redis import asyncio as aioredis
from redis.asyncio import Redis


class AsyncRedisStorage:
    def __init__(self, conn_cache: Redis):
        self._conn_cache = conn_cache
    # async def startup(self, *args, **kwargs):
    #     """Redis initialization method"""
    #     self._redis = await aioredis.from_url(*args, **kwargs)
    #
    # async def shutdown(self):
    #     """Redis connection termination method"""
    #     self._redis.close()
    #     await self._redis.wait_closed()

    async def get(self, key: str) -> str:
        """Method for getting data from Redis"""
        return await self._conn_cache.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        """Data persistence method in Redis"""
        await self._conn_cache.set(key, value, ex=expire)

    async def get_all_keys(self) -> Optional[list]:
        return await self._conn_cache.keys()

    async def get_all_values(self, keys: list) -> Optional[list]:
        if keys:
            return await self._conn_cache.mget(keys)
        return None

    async def delete(self, key: str):
        await self._conn_cache.delete(key)

    def create_key(self, params: list) -> Optional[str]:
        if params:
            str_key = ''.join([str(val) for val in params])
            return md5(str_key.encode("utf-8")).hexdigest()
        return None


cache: Optional[Redis] = None


async def get_cache() -> Optional[Redis]:
    """Function required for dependency injection"""
    return cache
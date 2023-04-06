from aiohttp import ClientSession
from typing import Optional
from core.config import settings
from urllib.parse import urljoin
from http import HTTPStatus
from fastapi import HTTPException
from json import loads


aio_client: Optional[ClientSession] = None


async def get_aio_client() -> Optional[ClientSession]:
    return aio_client


class AioSession:

    def __init__(self, aio_client: ClientSession):
        self.aio_client = aio_client
        self.base_url = f"http://{settings.line_provider.host}:{settings.line_provider.port}"

    async def execute_get(self, path: str = None):
        url_path = urljoin(self.base_url, path)
        response = await self.aio_client.get(url=url_path)
        if response.status == HTTPStatus.OK:
            data = await response.text()
            return loads(data)
        raise HTTPException(status_code=response.status, detail=response.reason)
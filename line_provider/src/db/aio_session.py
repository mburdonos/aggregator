import json

from aiohttp import ClientSession
from typing import Optional
from core.config import settings
from urllib.parse import urljoin
from http import HTTPStatus
from fastapi import HTTPException
from json import loads


class AioSession:

    def __init__(self):
        self.aio_client = ClientSession()
        self.base_url = f"http://{settings.bet_maker.host}:{settings.bet_maker.port}"

    async def execute_post(self, data: str, path: str = None):
        url_path = urljoin(self.base_url, path)
        response = await self.aio_client.post(
            url=url_path, data=data, headers={'Content-Type': 'application/json'}
        )
        if response.status == HTTPStatus.OK:
            data = await response.text()
            return data
        raise HTTPException(status_code=response.status, detail=response.reason)
import logging

import uvicorn
from aiohttp import ClientSession
from api.v1 import bet, events
from core.config import settings
from db import aio_session, db_cache, db_postgres
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Description API",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    db_postgres.pg_connection = create_async_engine(
        f"postgresql+asyncpg://{settings.storage_bet.user}:{settings.storage_bet.password}@{settings.storage_bet.host}:{settings.storage_bet.port}/{settings.storage_bet.dbname}",
        echo=True,
    )
    aio_session.aio_client = ClientSession()
    db_cache.cache = await aioredis.Redis(
        host=settings.cache_bet.host,
        port=settings.cache_bet.port,
        decode_responses=True,
    )
    # redis.exceptions.ConnectionError
    assert await db_cache.cache.ping()
    logging.info("Create connections")


@app.on_event("shutdown")
async def shutdown():
    await db_postgres.pg_connection.close()
    await aio_session.aio_client.close()
    if db_cache.cache:
        db_cache.cache.close()
        await db_cache.cache.wait_closed()
    logging.info("Closed connections")


app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(bet.router, prefix="/api/v1", tags=["Bet"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.bet_maker.host,
        port=settings.bet_maker.port,
        reload=True,
    )

import logging

import uvicorn
from api.v1 import events, bet
from core.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from db import db_postgres, aio_session
from aiohttp import ClientSession

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
    echo=True
    )
    aio_session.aio_client = ClientSession()
    logging.info("Create connections")


@app.on_event("shutdown")
async def shutdown():
    await db_postgres.pg_connection.close()
    await aio_session.aio_client.close()
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

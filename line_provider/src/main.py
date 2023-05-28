import logging

import uvicorn
from api.v1 import events
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from broker.message_broker import get_rabbitmq

from db import storage

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
    storage.pg_engine = create_async_engine(
        f"postgresql+asyncpg://{settings.storage_provider.user}:{settings.storage_provider.password}@{settings.storage_provider.host}:{settings.storage_provider.port}/{settings.storage_provider.dbname}",
        echo=True,
    )
    rabbitmq = get_rabbitmq()
    await rabbitmq.connect()
    logging.info("Create connections")


@app.on_event("shutdown")
async def shutdown():
    await storage.pg_engine.close()
    rabbitmq = get_rabbitmq()
    await rabbitmq.close()
    logging.info("Closed connections")

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.line_provider.host,
        port=settings.line_provider.port,
        reload=True,
    )

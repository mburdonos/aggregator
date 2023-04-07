import logging

import uvicorn
from api.v1 import events
from core.config import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Description API",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(events.router, prefix="/api/v1/events", tags=["events"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.line_provider.host,
        port=settings.line_provider.port,
        reload=True,
    )

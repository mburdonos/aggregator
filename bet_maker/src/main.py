import logging

import uvicorn
from api.v1 import events, bet
from core.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, ORJSONResponse

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
    logging.info("Create connections")


@app.on_event("shutdown")
async def shutdown():
    logging.info("Closed connections")


app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(bet.router, prefix="/api/v1", tags=["Bet"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.bet_marker.host,
        port=settings.bet_marker.port,
        reload=True,
    )

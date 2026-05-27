import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.database import check_postgres, check_redis
from app.services.ai import generate_reply

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

APP_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting API (env=%s)", settings.app_env)
    yield
    logger.info("Shutting down API")


app = FastAPI(
    title="Assignment AI API",
    description="FastAPI + PostgreSQL + Redis — local Docker stack",
    version=APP_VERSION,
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str
    provider: str


@app.get("/")
async def root():
    return {
        "service": "assignment-ai-api",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    db_ok, db_status = check_postgres()
    redis_ok, redis_status = check_redis()
    all_ok = db_ok and redis_ok
    body = {
        "status": "ok" if all_ok else "degraded",
        "version": APP_VERSION,
        "database": db_status,
        "redis": redis_status,
    }
    if not all_ok:
        raise HTTPException(status_code=503, detail=body)
    return body


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    reply, provider = await generate_reply(payload.message)
    return ChatResponse(reply=reply, provider=provider)

import logging
from typing import Optional, Tuple

import redis
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings

logger = logging.getLogger(__name__)

_engine: Optional[Engine] = None
_redis: Optional[redis.Redis] = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.database_url, pool_pre_ping=True)
    return _engine


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        settings = get_settings()
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def check_postgres() -> Tuple[bool, str]:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "connected"
    except SQLAlchemyError as exc:
        logger.warning("PostgreSQL health check failed: %s", exc)
        return False, "disconnected"


def check_redis() -> Tuple[bool, str]:
    try:
        get_redis().ping()
        return True, "connected"
    except redis.RedisError as exc:
        logger.warning("Redis health check failed: %s", exc)
        return False, "disconnected"

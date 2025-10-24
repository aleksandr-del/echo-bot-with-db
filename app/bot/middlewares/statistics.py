#!/usr/bin/env python3


import logging
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from app.infrastructure.database.db import update_user_activity
from psycopg import AsyncConnection
from .database import Handler, Data


logger = logging.getLogger(__name__)


class ActivityCounterMiddleware(BaseMiddleware):
    async def __call__(self, handler: Handler, event: Update, data: Data) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        result = await handler(event, data)

        conn: AsyncConnection | None = data.get("conn")
        if conn is None:
            logger.error("No database connection found in middleware data")
            raise RuntimeError
        await update_user_activity(conn=conn, user_id=user.id)

        return result

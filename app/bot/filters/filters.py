#!/usr/bin/env python3


import logging
from aiogram.types import CallbackQuery, Message
from aiogram.filters import BaseFilter
from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.infrastructure.database.db import get_user_role
from typing import TypeAlias

logger = logging.getLogger(__name__)
Event: TypeAlias = Message | CallbackQuery


class UserRoleFilter(BaseFilter):
    def __init__(self, *roles: str | UserRole) -> None:
        if not roles:
            logger.error(
                "At least one role must be provided to `%s`", self.__class__.__name__
            )
            raise ValueError
        self.roles = frozenset(
            UserRole(role) if isinstance(role, str) else role
            for role in roles
            if isinstance(role, (str, UserRole))
        )
        if not self.roles:
            logger.error("No valid roles provided to `%s`", self.__class__.__name__)

    async def __call__(self, event: Event, conn: AsyncConnection) -> bool:
        user = event.from_user
        if not user:
            return False
        role = await get_user_role(conn=conn, user_id=user.id)
        if role is None:
            return False
        return role in self.roles


class LocaleFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, locales: list[str]) -> bool:
        if isinstance(callback, CallbackQuery):
            logger.error(
                "LocaleFilter: expected `CallbackQuery`, got `%s`",
                callback.__class__.__name__,
            )
            raise TypeError
        return callback.data in locales

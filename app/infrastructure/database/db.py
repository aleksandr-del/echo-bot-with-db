#!/usr/bin/env python3


import logging
from datetime import datetime, timezone
from psycopg import AsyncConnection
from app.bot.enums.roles import UserRole
from typing import Any


logger = logging.getLogger(__name__)


async def add_user(
    conn: AsyncConnection,
    *,
    user_id: int,
    username: str | None = None,
    language: str = "ru",
    role: UserRole = UserRole.USER,
    is_alive: bool = True,
    banned: bool = False,
) -> None:
    async with conn.cursor() as cursor:
        query = """
            insert into users(user_id, username, language, role, is_alive, banned)
            values(
                %(user_id)s,
                %(username)s,
                %(language)s,
                %(role)s,
                %(is_alive)s,
                %(banned)s
            ) on conflict do nothing;
            """
        params = {
            "user_id": user_id,
            "username": username,
            "language": language,
            "role": role,
            "is_alive": is_alive,
            "banned": banned,
        }
        await cursor.execute(query=query, params=params)
        logger.info(
            (
                "User added. User_id=%s, created_at=%s, "
                "language=%s, role=%s, is_alive=%s, banned=%s"
            ),
            user_id,
            datetime.now(timezone.utc),
            language,
            role,
            is_alive,
            banned,
        )


async def get_user(conn: AsyncConnection, user_id: int) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        query = (
            "select id, user_id, username, language, role, is_alive, banned, created_at "
            "from users "
            "where user_id = %s"
        )
        params = (user_id,)
        data = await cursor.execute(query=query, params=params)
        row = await data.fetchone()
    logger.info("User is %s", row)
    return row if row else None


async def update_user_alive_status(
    conn: AsyncConnection, *, is_alive: bool, user_id: int
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="update users set is_alive = %s where user_id = %s",
            params=(is_alive, user_id),
        )
    logger.info("Updated `is_alive` status to %s for user %s", is_alive, user_id)


async def update_user_banned_status_by_id(
    conn: AsyncConnection, *, banned: bool, user_id: int
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="update users set banned = %s where user_id = %s",
            params=(banned, user_id),
        )
    logger.info("Updated `banned` status to %s for user %s", banned, user_id)


async def update_user_banned_status_by_username(
    conn: AsyncConnection, *, banned: bool, username: str
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="update users set banned = %s where username = %s",
            params=(banned, username),
        )
    logger.info("Updated `banned` status to %s for user %s", banned, username)


async def update_user_lang(
    conn: AsyncConnection, *, language: str, user_id: int
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="update users set language = %s where user_id = %s",
            params=(language, user_id),
        )
    logger.info("The language `%s` is set for the user %s", language, user_id)


async def get_user_lang(conn: AsyncConnection, *, user_id: int) -> str | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="select language from users where user_id = %s", params=(user_id,)
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the language `%s`", user_id, row[0])
    else:
        logger.info("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_user_alive_status(conn: AsyncConnection, *, user_id: int) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="select is_alive from users where user_id = %s", params=(user_id,)
        )
        row = await cursor.fetchone()
    if row:
        logger.info(
            "The user with `user_id`=%s has the is_alive status `%s`",
            user_id,
            row[0],
        )
    else:
        logger.info("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_user_banned_status_by_id(
    conn: AsyncConnection, *, user_id: int
) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="select banned from users where user_id = %s", params=(user_id,)
        )
        row = await cursor.fetchone()
    if row:
        logger.info(
            "The user with `user_id`=%s has the banned status `%s`", user_id, row[0]
        )
    else:
        logger.info("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def get_user_banned_status_by_username(
    conn: AsyncConnection, *, username: str
) -> bool | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="select banned from users where username = %s", params=(username,)
        )
        row = await cursor.fetchone()
    if row:
        logger.info(
            "The user with `username`=%s has the banned status `%s`", username, row[0]
        )
    else:
        logger.info("No user with `username`=%s found in the database", username)
    return row[0] if row else None


async def get_user_role(conn: AsyncConnection, *, user_id: int) -> str | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="select role from users where user_id = %s", params=(user_id,)
        )
        row = await cursor.fetchone()
    if row:
        logger.info("The user with `user_id`=%s has the role `%s`", user_id, row[0])
    else:
        logger.info("No user with `user_id`=%s found in the database", user_id)
    return row[0] if row else None


async def update_user_activity(conn: AsyncConnection, *, user_id: int) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query=(
                "insert into activity(user_id) values(%s) on "
                "conflict (user_id, activity_date) "
                "do update set actions = activity.actions + 1"
            ),
            params=(user_id,),
        )
    logger.info("User activity updated. Table=`activity`, user_id=%d", user_id)


async def get_statistics(conn: AsyncConnection) -> list[Any] | None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query=(
                "select user_id, sum(actions) as total_actions "
                "from activity group by user_id "
                "order by total_actions desc limit 5"
            )
        )
        rows = await cursor.fetchall()
    logger.info("Users activity fetched from table=`activity`")
    return [*rows] if rows else None

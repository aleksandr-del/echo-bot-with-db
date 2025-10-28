#!/usr/bin/env python3


import logging
from psycopg import AsyncConnection

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.bot.enums.roles import UserRole
from app.bot.filters.filters import UserRoleFilter
from app.infrastructure.database.db import (
    update_user_banned_status_by_id,
    update_user_banned_status_by_username,
    get_statistics,
    get_user_banned_status_by_id,
    get_user_banned_status_by_username,
)


logger = logging.getLogger(__name__)
admin_router = Router()
admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))


@admin_router.message(Command("help"))
async def process_help_command(message: Message, i18n: dict[str, str]) -> None:
    await message.answer(text=i18n.get("/help_admin"))


@admin_router.message(Command("statistics"))
async def process_statistics_command(
    message: Message, conn: AsyncConnection, i18n: dict[str, str]
) -> None:
    stats = await get_statistics(conn=conn)
    await message.answer(
        text=i18n.get("statistics").format(
            "\n".join(
                f"{i} <b>{stat[0]}</b>: {stat[1]}" for i, stat in enumerate(stats, 1)
            )
        )
    )


@admin_router.message(Command("ban"))
async def process_ban_command(
    message: Message,
    command: CommandObject,
    conn: AsyncConnection,
    i18n: dict[str, str],
) -> None:
    args = command.args
    if not args:
        await message.reply(text=i18n.get("empty_ban_answer"))
        return

    arg_user = args.split()[0].strip()
    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_id(
            conn=conn, user_id=int(arg_user)
        )
    elif arg_user.startswith("@"):
        banned_status = await get_user_banned_status_by_username(
            conn=conn, username=arg_user[1:]
        )
    else:
        await message.reply(text=i18n.get("incorrect_ban_arg"))
        return

    if banned_status is None:
        await message.reply(text=i18n.get("no_user"))
    elif banned_status:
        await message.reply(text=i18n.get("already_banned"))
    else:
        if arg_user.isdigit():
            await update_user_banned_status_by_id(
                conn=conn, banned=True, user_id=int(arg_user)
            )
        else:
            await update_user_banned_status_by_username(
                conn=conn, banned=True, username=arg_user[1:]
            )
        await message.reply(text=i18n.get("successfully_banned"))


@admin_router.message(Command("unban"))
async def process_unban_command(
    message: Message,
    command: CommandObject,
    conn: AsyncConnection,
    i18n: dict[str, str],
) -> None:
    args = command.args
    if not args:
        await message.reply(text=i18n.get("empty_unban_answer"))
        return

    arg_user = args.split()[0].strip()
    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_id(
            conn=conn, user_id=int(arg_user)
        )
    elif arg_user.startswith("@"):
        banned_status = await get_user_banned_status_by_username(
            conn=conn, username=arg_user[1:]
        )
    else:
        await message.reply(text=i18n.get("incorrect_unban_arg"))
        return

    if banned_status is None:
        await message.reply(text=i18n.get("no_user"))
    elif banned_status:
        if arg_user.isdigit():
            await update_user_banned_status_by_id(
                conn=conn, banned=False, user_id=int(arg_user)
            )
        else:
            await update_user_banned_status_by_username(
                conn=conn, banned=False, username=arg_user[1:]
            )
        await message.reply(text=i18n.get("successfully_unbanned"))
    else:
        await message.reply(text=i18n.get("not_banned"))

#!/usr/bin/env python3


import logging
from contextlib import suppress
from psycopg import AsyncConnection

from aiogram import Bot, Router
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BotCommandScopeChat,
    ChatMemberUpdated,
    Message,
    User,
)

from app.bot.enums.roles import UserRole
from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.states.states import LangSG
from app.infrastructure.database.db import (
    add_user,
    update_user_alive_status,
    get_user,
    get_user_lang,
)


logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    conn: AsyncConnection,
    bot: Bot,
    i18n: dict[str, str],
    state: FSMContext,
    adnin_ids: list[int],
    translations: dict[str, str],
) -> None:
    user: User | None = message.from_user
    user_row = await get_user(conn=conn, user_id=user.id)
    if user_row is None:
        user_role = UserRole.ADMIN if user.id in adnin_ids else UserRole.USER
        await add_user(
            conn=conn,
            user_id=user.id,
            username=user.username,
            language=user.language_code,
            role=user_role,
        )
    else:
        user_role = UserRole(user_row[4])
        await update_user_alive_status(conn=conn, is_alive=True, user_id=user.id)

    if await state.get_state() == LangSG.lang:
        data = await state.get_data()
        with suppress(TelegramBadRequest):
            msg_id = data.get("lang_settings_msg_id")
            if msg_id:
                await bot.edit_message_reply_markup(chat_id=user.id, message_id=msg_id)
        user_lang = await get_user_lang(conn=conn, user_id=user.id)
        i18n = translations.get(user_lang)

    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n, role=user_role),
        scope=BotCommandScopeChat(type=BotCommandScopeType.CHAT, chat_id=user.id),
    )
    await message.answer(text=i18n.get("/start"))
    await state.clear()


@user_router.message(Command("help"))
async def process_help_command(message: Message, i18n: dict[str, str]) -> None:
    message.answer(text=i18n.get("/help"))


@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(
    event: ChatMemberUpdated, conn: AsyncConnection
) -> None:
    logger.info("User `%d` blocked the bot", event.from_user.id)
    await update_user_alive_status(
        conn=conn, is_alive=False, user_id=event.from_user.id
    )

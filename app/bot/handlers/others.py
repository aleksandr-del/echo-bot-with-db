#!/usr/bin/env python3


from aiogram import Router
from aiogram.types import Message


others_router = Router()


@others_router.message()
async def send_echo(message: Message, i18n: dict[str, str]) -> None:
    try:
        await message.send_copy(chat_id=message.from_user.id)
    except TypeError:
        await message.answer(text=i18n.get("no_echo"))

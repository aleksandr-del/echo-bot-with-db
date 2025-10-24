#!/usr/bin/env python3

import logging.config
from app.logger.logging_settings import logging_config

logging.config.dictConfig(logging_config)

from config.config import Config, load_config
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommandScopeChat
from aiogram.enums import BotCommandScopeType
from aiogram.filters import CommandStart
from locales.ru.txt import RU
from app.bot.keyboards.menu_button import get_main_menu_commands
from app.bot.enums.roles import UserRole

config: Config = load_config()
bot = Bot(config.bot.token)
dp = Dispatcher()
dp.workflow_data.update({"admin_ids": config.bot.admin_ids})


@dp.message(CommandStart())
async def process_start_command(
    message: Message, bot: Bot, admin_ids: list[int]
) -> None:
    role = UserRole.ADMIN if message.from_user.id in admin_ids else UserRole.USER
    await bot.set_my_commands(
        commands=get_main_menu_commands(RU, role),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT, chat_id=message.from_user.id
        ),
    )
    await message.answer(text=RU[message.text])


if __name__ == "__main__":
    dp.run_polling(bot)

#!/usr/bin/env python3


from aiogram.types import BotCommand
from app.bot.enums.roles import UserRole


def get_main_menu_commands(i18n: dict[str, str], role: UserRole):
    commands = "start lang help ban unban statistics".split()
    buttons = [
        BotCommand(
            command=f"/{command}", description=i18n.get(f"/{command}_description")
        )
        for command in commands
    ]
    return buttons if role == UserRole.ADMIN else buttons[:3]

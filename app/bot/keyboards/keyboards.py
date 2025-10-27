#!/usr/bin/env python3


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_lang_settings_kb(
    i18n: dict, locales: list[str], checked: str
) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = []

    for locale in sorted(locales):
        if locale == "default":
            continue
        if locale == checked:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"🔘 {i18n.get(locale)}", callback_data=locale
                    )
                ]
            )
        else:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"⚪️ {i18n.get(locale)}", callback_data=locale
                    )
                ]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    text="cancel_lang_button_text",
                    callback_data="cancel_lang_button_data",
                ),
                InlineKeyboardButton(
                    text="save_lang_button_text", callback_data="save_lang_button_data"
                ),
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=buttons)

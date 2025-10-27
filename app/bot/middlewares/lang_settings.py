import logging
from typing import Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Update, User, callback_query

from .database import Data, Handler

logger = logging.getLogger(__name__)


class LangSettingsMiddlware(BaseMiddleware):
    async def __call__(self, handler: Handler, event: Update, data: Data) -> Any:
        user: User | None = data.get("event_fron_user")
        if user is None:
            return await handler(event, data)

        if event.callback_query is None:
            return await handler(event, data)

        locales: list[str] | None = data.get("locales")
        state: FSMContext | None = data.get("state")
        user_context_data: dict = await state.get_data()

        if event.callback_query.data == "cancel_lang_button":
            user_context_data.update(user_lang=None)
            await state.set_data(user_context_data)
        elif (
            event.callback_query.data in locales
            and event.callback_query.data != user_context_data.get("user_lang")
        ):
            user_context_data.update(user_lang=event.callback_query.data)
            await state.set_data(user_context_data)

        return await handler(event, data)

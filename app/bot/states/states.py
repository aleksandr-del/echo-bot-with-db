#!/usr/bin/env python3


from aiogram.fsm.state import State, StatesGroup


class LangSG(StatesGroup):
    lang = State()

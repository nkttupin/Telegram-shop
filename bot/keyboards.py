from typing import List

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.db.models import Category


async def start_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Каталог"),
            types.KeyboardButton(text="Корзина")
        ],
        [
            types.KeyboardButton(text="Заказы"),
            types.KeyboardButton(text="Связаться с Серегой")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        # input_field_placeholder=" способ подачи"
    )
    return keyboard


async def build_keyboard(categories:[]) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = []
    for cat in categories:
        buttons.append([cat.name])  # Каждая кнопка в отдельном списке

    buttons.append(["На главную"])
    buttons.append(["Назад"])
    for button_text in buttons:
        text = button_text[0]
        builder.add(types.KeyboardButton(text=text))  # Каждый элемент списка - это отдельная кнопка

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=False)

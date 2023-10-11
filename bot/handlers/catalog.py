import os
import sys

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db.find_catalog import find_category, find_categories_on_parent, find_category_id
from bot.handlers.main_handler import FSM_status
from bot.keyboards import start_keyboard, build_keyboard

router = Router()


@router.message(FSM_status.catalog_menu, F.text == 'На главную')
async def go_start(message: Message, state: FSMContext):
    await message.answer('На главную', reply_markup=await start_keyboard())
    await state.set_state(FSM_status.main_menu)


@router.message(FSM_status.catalog_menu, F.text == 'Назад')
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    cat = data.get('catalog_menu')
    print(cat.parent_category_id)
    if cat.parent_category_id is None:
        await go_start(message, state)
    else:
        parent_cat = await find_category_id(session, cat.parent_category_id)
        await get_category_keyboard(message, session, state, parent_cat)


# Нужно вынести вывод продуктов и категорий в отдельную функцию
@router.message(FSM_status.catalog_menu, F.text)
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    cat = await find_category(session=session, name=message.text)
    if cat:
        await get_category_keyboard(message, session, state, cat)
    else:
        await message.answer('Прости, не понял какая категория тебе нужна')
        return

        # Найти такой объект в базе и вывести кнопки подкатегорий
    await message.answer("Если есть, то продукты в инлайн выводим")


async def get_category_keyboard(message: Message, session: AsyncSession, state: FSMContext, category):
    """ По существующему объекту Category выводим
    Подкатегории в кнопки    """
    await state.update_data(catalog_menu=category)
    categories = await find_categories_on_parent(session, category)

    # data = await state.get_data()
    # catalog_menu = data.get('catalog_menu')
    # print(catalog_menu)

    await message.answer_photo(
        category.img_url,
        caption=category.name
    )
    await message.answer(message.text, reply_markup=await build_keyboard(categories))

import os
import sys

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db.find_catalog import get_actual_meta, main_category, main_category
from bot.keyboards import start_keyboard, build_keyboard

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

router = Router()


class FSM_status(StatesGroup):
    main_menu = State()
    catalog_menu = State()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    await message.answer("Приветики", reply_markup=await start_keyboard())
    await state.set_state(FSM_status.main_menu)


@router.message(F.text == 'Каталог')
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    # Вывести кнопки какие есть
    cat = await main_category(session)
    await message.answer('Каталог', reply_markup=await build_keyboard(cat))
    await state.set_state(FSM_status.catalog_menu)

@router.message()
async def echo(message: Message):
    await message.reply(f'Не понял твою команду, можешь начать заново - /start')

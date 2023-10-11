import os
import sys

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db.commands import db_get_all_users
from bot.keyboards import start_keyboard, build_keyboard

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from bot.db.models import User
from bot.filters.admin import UserInGroupFilter

router = Router(name='admin_commands')
router.message.filter(
    UserInGroupFilter(group_type="admins")
)

@router.message(F.text == '/users')
async def get_users(message: Message, session: AsyncSession):
    users = await db_get_all_users(message, session)
    await message.answer(users)

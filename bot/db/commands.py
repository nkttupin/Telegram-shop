import datetime
import os
import sys

from aiogram import Router
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_session, async_sessionmaker
from aiogram.dispatcher import router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, and_, exists
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

# Add the path to the bot package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import from the bot package
from bot.db.models import User, User_group, association_table, Message as DBMessage
from sqlalchemy.orm import Session


async def check_user_group(from_user_id: int, group_type: str, session: AsyncSession) -> bool:
    sql = await session.execute(
        select(User_group).where(User_group.group_name == group_type))

    # СЮДА ДОБАВИТЬ УСЛОВИЕ,ЕСТЬ ЛИ ЮЗЕР В ГРУППЕ
    group_user = sql.scalars().first()
    print(from_user_id)
    sql = await session.execute(
        select(User).where(User.telegram_id == from_user_id))
    user = sql.scalars().first()

    if not user or not group_user:
        return False

    ql = await session.execute(
        select(association_table).join(User_group).join(User)
        .where(User_group.group_name == group_type)
        .where(User.id == user.id))
    result = ql.scalars().first()

    if result:
        return True
    else:
        return False


async def check_user(from_user_id: int, session: AsyncSession) -> bool:
    """
       Проверяет, есть ли пользователь с указанным идентификатором в базе данных.
       :param from_user_id: Идентификатор из телеграмма
       :param session: Сессия базы данных
       :return: True, если пользователь уже есть в базе, иначе - False
    """
    sql = await session.execute(
        select(User).where(User.telegram_id == from_user_id))
    answer = sql.scalars().first()
    print(answer)
    if answer:
        return True
    else:
        return False


async def create_user(message: Message, session: AsyncSession):
    is_exist = await check_user(message.from_user.id, session)

    if is_exist:
        # await message.answer("рад твоему возращению")
        return

    sql = await session.execute(
        select(User_group).where(User_group.group_name == "users"))
    group = sql.scalars().first()

    await session.merge(User(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        is_bot=message.from_user.is_bot,
        language_code=message.from_user.language_code,

        groups=[group]
    ))
    await session.commit()



async def save_message(message: Message, session: AsyncSession):
    sql = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id))
    user = sql.scalars().first()
    if not user:
        return

    await session.merge(DBMessage(
        datetime=datetime.datetime.now(),
        text=message.text,
        user=user,
    ))
    await session.commit()
    # await message.answer("добавил в базу)")


async def db_get_all_users(message: Message, session: AsyncSession):
    """ получение всех юзеров """

    sql = select(User)
    # sql = await session.execute(select(User).where(User.telegram_id == message.from_user.id))

    users_sql = await session.execute(sql)
    users = users_sql.scalars()

    users_list = '\n'.join([f'{index + 1}. {item.telegram_id}' for index, item in enumerate(users)])

    return users_list


async def get_user(message: Message, session: AsyncSession):
    sql = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id))
    user = sql.scalars().first()
    if user:
        return user
    else:
        return


async def save_geo_position(message: Message, session: AsyncSession):
    user = await get_user(message, session)
    if user:
        user.geo_position = f"{message.location.longitude};{message.location.latitude}"
        await session.commit()
        await message.answer(f'Добавлена геолокация\nЖди в гости😎')

    else:
        await message.answer("Что то не так с юзером")

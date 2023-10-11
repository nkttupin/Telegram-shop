import os
import sys
from typing import List

from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, and_, exists, desc
from sqlalchemy.ext.asyncio import AsyncSession

# Add the path to the bot package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import from the bot package
from bot.db.models import User, User_group, association_table, Category, Meta_Upgrade
from sqlalchemy.orm import Session


async def get_actual_meta(session: AsyncSession) -> Meta_Upgrade:
    sql_meta = await session.execute(select(Meta_Upgrade)
                                     .order_by(desc(Meta_Upgrade.created_at)))
    meta = sql_meta.scalars().first()
    return meta


async def find_category(session: AsyncSession, name: str):
    sql = await session.execute(
        select(Category).where(Category.name == name).
        where(Category.meta_upgrade == await get_actual_meta(session)))
    category = sql.scalars().first()

    if category is None:
        return None  # Return None if the category is not found

    return category

async def find_category_id(session: AsyncSession, id: int):
    sql = await session.execute(
        select(Category).where(Category.id == id).
        where(Category.meta_upgrade == await get_actual_meta(session)))
    category = sql.scalars().first()

    if category is None:
        return None  # Return None if the category is not found

    return category


async def main_category(session: AsyncSession):
    sql = await session.execute(
        select(Category).where(Category.parent_category_id == None).
        where(Category.meta_upgrade == await get_actual_meta(session)))
    category = sql.scalars().all()

    return category


async def find_categories(session: AsyncSession, names: List[str]):
    categories = []
    for name in names:
        sql = await session.execute(
            select(Category).where(Category.name == name).
            where(Category.meta_upgrade == await get_actual_meta(session)))
        category = sql.scalars().first()
        if category:
            categories.append(category)

    return categories


async def find_categories_on_parent(session: AsyncSession, parentCat: Category):


    sql = await session.execute(
        select(Category).where(Category.parent_category_id == parentCat.id).
        where(Category.meta_upgrade == await get_actual_meta(session)))
    categories = sql.scalars().all()

    return categories

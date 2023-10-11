from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.commands import check_user_group


class UserInGroupFilter(BaseFilter):
    def __init__(self, group_type: str):
        self.group_type = group_type

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return await check_user_group(message.from_user.id,self.group_type, session)

from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.commands import check_user_group, create_user, save_message


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            if isinstance(event.event, Message):
                message = event.event
                # Проверка на забененного пользователя
                isbanned = await check_user_group(message.from_user.id, "banned", session)
                # Проверяем на приматность чата и чтоб пользователь не был ботом и забаненным
                if isbanned or message.chat.type != 'private' or message.from_user.is_bot == True:
                    await message.answer(f"ты в бане, лох ")
                    return
                #await message.answer(f"фух ты не в бане")

                # Добавляем нового если нет такого
                await create_user(message,session)
                # Сохраняем в бд сообщение
                await save_message(message,session)


            return await handler(event, data)

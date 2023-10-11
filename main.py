# This is a sample Python script.
import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.handlers import main_handler, catalog, admin
from bot.middlewares.dbMiddleware import DbSessionMiddleware

load_dotenv()


async def on_startup(bot):
    scheduler = AsyncIOScheduler(timezone = "UTC")
    # scheduler.add_job(functools.partial(message_admin, bot), 'cron', hour=3, minute=0)
    scheduler.start()


async def main():

    engine = create_async_engine(url=os.getenv('DB_URL'), echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=os.getenv('BOT_TOKEN'))

    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    dp.include_routers(admin.router, catalog.router, main_handler.router )
   # dp.include_routers(main_handler.router)
    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    # await ui_commands.set_ui_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход из бота')

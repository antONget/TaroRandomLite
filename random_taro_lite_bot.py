from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from handlers import error, other_handlers, start_handler
from handlers.partner import handler_publish_card, handler_partner_group
from handlers.admin import handler_edit_list_personal
from handlers.group import handler_show_random_card
from utils import load_photo
from notify_admins import on_startup_notify
from database.models import async_main

import asyncio
import logging


logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    """
    Основной файл для запуска
    :return:
    """
    await async_main()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        # filename="py_log.log",
        # filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await on_startup_notify(bot=bot)
    # Регистрируем router в диспетчере
    dp.include_router(error.router)
    dp.include_router(start_handler.router)
    dp.include_router(load_photo.router)
    dp.include_routers(handler_show_random_card.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

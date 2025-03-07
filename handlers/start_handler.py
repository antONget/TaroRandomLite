from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config_data.config import Config, load_config
from database import requests as rq
from database.models import User, Card
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin

import logging
import random

router = Router()
config: Config = load_config()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message, state: FSMContext, command: CommandObject, bot: Bot) -> None:
    """
    Обработки запуска бота или ввода команды /start
    :param message:
    :param state:
    :param command:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.chat.id}')
    await state.set_state(state=None)
    # добавление пользователя в БД если еще его там нет
    user: User = await rq.get_user_by_id(tg_id=message.from_user.id)
    if not user:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "name": username}
        if await check_super_admin(telegram_id=message.from_user.id):
            data_user = {"tg_id": message.from_user.id,
                         "name": username,
                         "role": rq.UserRole.admin}
        await rq.add_user(data=data_user)
    user: User = await rq.get_user_by_id(tg_id=message.from_user.id)
    if user.active:
        await message.answer(text='Привет! Я - ясновидящий и могу предсказывать будущее🪬\n\n'
                                  'Могу погадать в личке через команду /картадня, но лучше всего меня добавить'
                                  ' в групповой чат с твоими друзьями и также вызывать через команду /картадня'
                                  ' - тогда вы сможете совместно обсудить и строить планы💅🏻')
    else:
        await message.answer(text='Для доступа к функционалу бота, пришлите кодовое слово.')


@router.message(F.text == 'Ведьминская гуща')
@error_handler
async def cod_word(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обработки запуска бота или ввода команды /start
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'cod_word: {message.chat.id}')
    await rq.set_user_active(tg_id=message.from_user.id)
    await message.answer(text='Привет! Я - ясновидящий и могу предсказывать будущее🪬\n\n'
                              'Могу погадать в личке через команду /картадня, но лучше всего меня добавить'
                              ' в групповой чат с твоими друзьями и также вызывать через команду /картадня'
                              ' - тогда вы сможете совместно обсудить и строить планы💅🏻')


@router.message(F.text == '/картадня')
@error_handler
async def process_load_card(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск загрузки фото
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_load_card: {message.chat.id}')
    user: User = await rq.get_user_by_id(tg_id=message.from_user.id)
    if user.active:
        list_cards = await rq.get_cards()
        if list_cards:
            random_card: Card = random.choice(list_cards)
            await message.answer_photo(photo=random_card.photo_id,
                                       caption=random_card.description)
            await message.delete()
    else:
        await message.answer(text='Для доступа к функционалу бота, пришлите кодовое слово.')

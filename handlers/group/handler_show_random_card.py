from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config_data.config import Config, load_config
from database import requests as rq
from database.models import Card, Group
from utils.error_handling import error_handler
from filter.groups_chat import IsGroup

import logging
import random

router = Router()
config: Config = load_config()


class StateLoadCard(StatesGroup):
    load_card = State()


@router.message(F.text == '/картадня', IsGroup())
@error_handler
async def process_load_card(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск загрузки фото
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_load_card: {message.from_user.id}')
    group: Group = await rq.get_group_peer_id(peer_id=message.chat.id)
    if not group:
        await rq.add_group(group_id=message.chat.id, data={"group_id": message.chat.id,
                                                           "active": 0})
        await message.answer(text='Для доступа к карте дня пришлите кодовое слово')
    elif group.active:
        list_cards = await rq.get_cards()
        if list_cards:
            random_card: Card = random.choice(list_cards)
            await message.answer_photo(photo=random_card.photo_id,
                                       caption=random_card.description)
            await message.delete()
    else:
        await message.answer(text='Для доступа к карте дня пришлите кодовое слово')


@router.message(F.text == 'Ведьминская гуща', IsGroup())
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
    group: Group = await rq.get_group_peer_id(peer_id=message.chat.id)
    if not group:
        await rq.add_group(group_id=message.chat.id, data={"group_id": message.chat.id,
                                                           "active": 1})
    else:
        await rq.set_group_active(group_id=message.chat.id)
        await message.answer(text='Группа активирована в боте @coffeegroundstalk_bot')

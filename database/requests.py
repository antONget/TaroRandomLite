from database.models import User, Card, Token, Group, async_session
from sqlalchemy import select
from dataclasses import dataclass
import logging


""" USER """


@dataclass
class UserRole:
    user = "user"
    admin = "admin"
    partner = "partner"


async def add_user(data: dict) -> None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            session.add(User(**data))
            await session.commit()
        else:
            user.username = data['username']
            await session.commit()


async def get_user_by_id(tg_id: int) -> User:
    """
    Получение информации о пользователе по tg_id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user_by_id {tg_id}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_id(id_: int) -> User:
    """
    Получение информации о пользователе id
    :param id_:
    :return:
    """
    logging.info(f'get_user_id {id_}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.id == id_))


async def set_user_role(tg_id: int, role: str) -> None:
    """
    Обновление роли пользователя
    :param tg_id:
    :param role:
    :return:
    """
    logging.info('set_user_phone')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.role = role
            await session.commit()


async def set_user_active(tg_id: int) -> None:
    """
    Авторизация пользователя
    :param tg_id:
    :return:
    """
    logging.info('set_user_active')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.active = 1
            await session.commit()


async def get_users_role(role: str) -> list[User]:
    """
    Получение списка пользователей с заданной ролью
    :param role:
    :return:
    """
    logging.info('get_users_role')
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.role == role))
        list_users = [user for user in users]
        return list_users


""" CARD """


async def add_card(data: dict) -> None:
    """
    Добавление токена
    :param data:
    :return:
    """
    logging.info(f'add_token')
    async with async_session() as session:
        new_card = Card(**data)
        session.add(new_card)
        await session.commit()


async def get_card(id_: int) -> Card:
    """
    Получение карты таро по id
    :param id_:
    :return:
    """
    logging.info('get_token')
    async with async_session() as session:
        return await session.scalar(select(Card).filter(Card.id == id_))


async def set_card_description(id_: int, description: str) -> None:
    """
    Обновление описание карты
    :param id_:
    :param description:
    :return:
    """
    logging.info('set_card_description')
    async with async_session() as session:
        card = await session.scalar(select(Card).filter(Card.id == id_))
        if card:
            card.description = description
            await session.commit()


async def get_cards() -> list[Card]:
    """
    Получение списка карт таро
    :return:
    """
    logging.info('get_token')
    async with async_session() as session:
        cards = await session.scalars(select(Card))
        return [card for card in cards]


""" TOKEN """


async def add_token(data: dict) -> None:
    """
    Добавление токена
    :param data:
    :return:
    """
    logging.info(f'add_token')
    async with async_session() as session:
        new_token = Token(**data)
        session.add(new_token)
        await session.commit()


async def get_token(token: str, tg_id: int) -> bool | str:
    """
    Проверка валидности токена
    :param token:
    :param tg_id:
    :return:
    """
    logging.info('get_token')
    async with async_session() as session:
        token_ = await session.scalar(select(Token).filter(Token.token == token))
        if token_:
            token_.tg_id = tg_id
            role = token_.role
            await session.commit()
            return role
        else:
            return False


async def delete_card(id_: int) -> bool:
    """
    Удаленеи карты таро по id
    :param id_:
    :return:
    """
    logging.info('get_token')
    async with async_session() as session:
        card = await session.scalar(select(Card).where(Card.id == id_))
        if card:
            await session.delete(card)
            await session.commit()
            return True


""" GROUP """


async def add_group(group_id: int, data: dict) -> None:
    """
    Добавляем новую группу либо обновляем ее название
    :param group_id:
    :param data:
    :return:
    """
    logging.info(f'add_manager')
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.group_id == group_id))
        if not group:
            session.add(Group(**data))
            await session.commit()


async def set_group_active(group_id: int) -> None:
    """
    Активация группы
    :param group_id:
    :param data:
    :return:
    """
    logging.info(f'set_group_active {group_id}')
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.group_id == group_id))
        if group:
            group.active = 1
            await session.commit()


async def get_group_peer_id(peer_id: int) -> Group:
    """
    Получаем группу по peer_id
    :return:
    """
    logging.info(f'get_group_peer_id')
    async with async_session() as session:
        return await session.scalar(select(Group).where(Group.group_id == peer_id))


async def delete_group(id_: int):
    """
    Удаление группы
    :param id_: id группы
    :return:
    """
    logging.info(f'delete_user')
    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.id == id_))
        if group:
            await session.delete(group)
            await session.commit()
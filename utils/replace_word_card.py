from database.models import Card
from database.requests import get_cards, set_card_description
import asyncio


async def replace_word_card():
    cards: list[Card] = await get_cards()
    for card in cards:
        description = card.description.replace('карту', '')
        await set_card_description(id_=card.id, description=description)


if __name__ == '__main__':
    asyncio.run(replace_word_card())

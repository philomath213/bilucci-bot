import os
import logging
from random import choice

from telegram.ext import (
    Updater,
    CommandHandler,
)


# BOT_API_TOKEN
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN", None)

logging.basicConfig(
    format='[+] [%(asctime)s] %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

# Spoils list
SPOILS = [
    "No spoilers for the moment"
]

# Quotes list
QUOTES = [
    "Tommy Shelby: I don't pay for suits",
    "Walter White: I am the danger.",
    "Tyrion Lannister: A lannister always pays his debts",
    "Jaqen H'Ghar: Valar Morghulis",
    "John Snow: I don't want it",
]


def start_spoiling(update, context):
    user = update.effective_user
    logger.info(f"{user.username} triggers start_spoiling")

    spoil = choice(SPOILS)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=spoil
    )

    logger.info(f"start_spoiling: {spoil}")


def gimme_quote(update, context):
    user = update.effective_user
    logger.info(f"{user.username} triggers gimme_quote")

    quote = choice(QUOTES)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=quote
    )
    logger.info(f"gimme_quote: {quote}")


def main():
    updater = Updater(token=BOT_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_spoiling_handler = CommandHandler('start_spoiling', start_spoiling)
    dispatcher.add_handler(start_spoiling_handler)

    logger.info("add 'start_spoiling' handler")

    gimme_quote_handler = CommandHandler('gimme_quote', gimme_quote)
    dispatcher.add_handler(gimme_quote_handler)

    logger.info("add 'gimme_quote' handler")

    updater.start_polling()


if __name__ == "__main__":
    main()

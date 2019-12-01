import logging
from random import choice

from telegram.ext import (
    Updater,
    CommandHandler,
)


# BOT API key
API_KEY = ""

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
    spoil = choice(SPOILS)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=spoil
    )


def gimme_quote(update, context):
    quote = choice(QUOTES)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=quote
    )


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token=API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    start_spoiling_handler = CommandHandler('start_spoiling', start_spoiling)
    dispatcher.add_handler(start_spoiling_handler)

    gimme_quote_handler = CommandHandler('gimme_quote', gimme_quote)
    dispatcher.add_handler(gimme_quote_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()

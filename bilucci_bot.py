import os
import logging
from random import choice

from telegram.ext import (
    Updater,
    CommandHandler,
)

import datamuse


# BOT_API_TOKEN
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN", None)

datamuse_api = datamuse.Datamuse()

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


GOOD_NIGHT_MSG = [
    "Good Night Alphabit Family",
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


def synonyms(update, context):
    user = update.effective_user

    if context.args:
        word = context.args[0].strip()
        logger.info(f"{user.username} triggers synonyms: {word}")

        syns = datamuse_api.words(rel_syn=word, max=10)
        if syns:
            msg = '\n'.join(map(lambda s: s['word'], syns))
        else:
            msg = f"can't find synonyms for {word}"
    else:
        msg = "/synonyms <word>"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg
    )

    logger.info("synonyms: %r" % msg)


def good_night(update, context):
    user = update.effective_user
    logger.info(f"{user.username} triggers good_night")

    good_night_msg = choice(GOOD_NIGHT_MSG)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=good_night_msg
    )
    logger.info(f"good_night: {good_night_msg}")


def main():
    updater = Updater(token=BOT_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_spoiling_handler = CommandHandler('start_spoiling', start_spoiling)
    dispatcher.add_handler(start_spoiling_handler)
    logger.info("add 'start_spoiling' handler")

    gimme_quote_handler = CommandHandler('gimme_quote', gimme_quote)
    dispatcher.add_handler(gimme_quote_handler)
    logger.info("add 'gimme_quote' handler")

    synonyms_handler = CommandHandler('synonyms', synonyms)
    dispatcher.add_handler(synonyms_handler)
    logger.info("add 'synonyms' handler")

    good_night_handler = CommandHandler('good_night', good_night)
    dispatcher.add_handler(good_night_handler)
    logger.info("add 'good_night' handler")

    updater.start_polling()


if __name__ == "__main__":
    main()

import os
import logging
from random import choice

from telegram.ext import (
    Updater,
    CommandHandler,
)

import datamuse

import omdb


# PORT
PORT = int(os.environ.get('PORT', '8443'))
# Heroku Application Name
APP_NAME = os.environ.get('APP_NAME', None)
# BOT_API_TOKEN
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN", None)

WEBHOOK_URL = f"https://{APP_NAME}.herokuapp.com/{BOT_API_TOKEN}"

# omdb API KEY
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", None)

# setup 3rd party APIs
omdb.set_default('apikey', OMDB_API_KEY)
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


ESI_CINAME_MSG = [
    "In this week's ESI Cinema we will watch:\nThe Irishman (2019) • Movie \n3h29min ⭐️8.7 IMDB\n\nDirector: Martin Scorsese\nActors: Robert De Niro, Al Pacino, Anna Paquin, Jesse Plemons\nGenres: Biography, 🔪 Crime, 🎭 Drama\nThe Irishman is a movie starring Robert De Niro, Al Pacino, and Anna Paquin. A mob hitman recalls his possible involvement with the slaying of Jimmy Hoffa."
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


def esi_cinema(update, context):
    user = update.effective_user
    logger.info(f"{user.username} triggers esi_cinema")

    esi_cinema_msg = choice(ESI_CINAME_MSG)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=esi_cinema_msg
    )
    logger.info(f"esi_cinema: {esi_cinema_msg}")


def what_movie(update, context):
    user = update.effective_user

    if context.args:
        title = ' '.join(context.args).strip()
        logger.info(f"{user.username} triggers what_movie: {title}")

        movie_info = omdb.request(t=title)
        if movie_info:
            msg = ""
            for x, y in movie_info.json().items():
                if x == 'Ratings':
                    ratings = "Ratings:\n"
                    for r in y:
                        ratings += f"    {r['Source']}: {r['Value']}\n"
                    msg += ratings
                else:
                    msg += f"{x}: {y}\n"
        else:
            msg = f"can't find movie {title}"
    else:
        msg = "/what_movie <title>"

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg
    )

    logger.info("what_movie: %r" % msg)


def help_cmd(update, context):
    text = "The following commands are available:\n"

    commands = [
        ["/start_spoiling", "Start spoiling"],
        ["/gimme_quote", "Get a randome quote"],
        ["/synonyms <word>", "Get list of Synonyms for word"],
        ["/good_night", "Say Good Night"],
        ["/esi_cinema", "Show ESI Cinema next Movie"],
        ["/what_movie", "Get informations about that movie"],
        ["/help", "Get this message"],
    ]

    for command in commands:
        text += command[0] + " " + command[1] + "\n"

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text
    )


def main():
    updater = Updater(token=BOT_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    help_cmd_handler = CommandHandler('help', help_cmd)
    dispatcher.add_handler(help_cmd_handler)
    logger.info("add 'help_cmd' handler")

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

    esi_cinema_handler = CommandHandler('esi_cinema', esi_cinema)
    dispatcher.add_handler(esi_cinema_handler)
    logger.info("add 'esi_cinema' handler")

    what_movie_handler = CommandHandler('what_movie', what_movie)
    dispatcher.add_handler(what_movie_handler)
    logger.info("add 'what_movie' handler")

    logger.info(f"PORT: {PORT}")
    logger.info(f"WEBHOOK_URL: {WEBHOOK_URL}")

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=BOT_API_TOKEN)
    updater.bot.set_webhook(WEBHOOK_URL)
    updater.idle()


if __name__ == "__main__":
    main()

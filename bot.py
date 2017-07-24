import logging
import os

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

import requests
from lxml import html


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

TOKEN = os.environ.get('OPPAI_BOT_TOKEN')


def get_media():
    API = 'https://twitter.com/i/profiles/show/Strangestone/media_timeline'
    rsp = requests.get(API)
    nodes = html.fromstring(rsp.json()['items_html'])
    imgs = nodes.xpath('//div[@class="AdaptiveMedia-container"]//img/@src')
    return imgs


updater = Updater(token=TOKEN)
bot = telegram.Bot(token=TOKEN)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Try some commands!")


start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)


def oppai(bot, update):
    media = get_media()
    bot.send_photo(chat_id=update.message.chat_id, photo=media[0])


def more_oppai(bot, update):
    media = get_media()
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Here comes %d oppais!" % len(media))
    for photo in media:
        bot.send_photo(chat_id=update.message.chat_id, photo=photo)


oppai_handler = CommandHandler('oppai', oppai)
updater.dispatcher.add_handler(oppai_handler)
more_oppai_handler = CommandHandler('more_oppai', more_oppai)
updater.dispatcher.add_handler(more_oppai_handler)


updater.start_polling()
updater.idle()

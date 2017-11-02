import logging
import os

from aiotg import Bot, Chat
import aiohttp

from lxml import html

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

TOKEN = os.environ.get('OPPAI_BOT_TOKEN')
bot = Bot(api_token=TOKEN)
bot.session._trust_env = True    # Using HTTP_PROXY

TIMELINE_API = 'https://twitter.com/i/profiles/show/Strangestone/media_timeline'
TWEET_NODES_XPATH = '//li/div[contains(@class, "tweet")]/div[contains(@class, "content")]'
TWEET_PHOTO_XPATH = 'div//div[contains(@class, "js-adaptive-photo")]/img/@src'
TWEET_TEXT_XPATH = 'div//p[contains(@class, "tweet-text")]/text()'


async def get_media():
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(TIMELINE_API) as rsp:
            content_json = await rsp.json()
    nodes = html.fromstring(content_json['items_html'])
    tweet_nodes = nodes.xpath(TWEET_NODES_XPATH)
    tweets = map(lambda node: { 'photo': node.xpath(TWEET_PHOTO_XPATH)[0],
                                'caption': node.xpath(TWEET_TEXT_XPATH)[0] },
                 tweet_nodes)
    oppai_tweets = list(filter(lambda x: '月曜日のたわわ' in x['caption'], tweets))
    return oppai_tweets


@bot.command('/start')
async def start(chat: Chat, match):
    chat.reply('''
Try some commands!
''')


@bot.command('/oppai')
async def oppai(chat: Chat, match):
    media = await get_media()
    await chat.send_photo(photo=media[0]['photo'], caption=media[0]['caption'])


@bot.command('/more_oppai')
async def more_oppai(chat: Chat, match):
    media = await get_media()
    chat.reply('Here comes %d oppais!' % len(media))
    for i in media:
        await chat.send_photo(photo=i['photo'], caption=i['caption'])


if __name__ == '__main__':
    bot.run(debug=True)

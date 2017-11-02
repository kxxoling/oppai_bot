import os
import json

import pytest
from lxml import html

from bot import TIMELINE_API, TWEET_PHOTO_XPATH, TWEET_TEXT_XPATH, TWEET_NODES_XPATH

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TWITTER_TIMELINE_JSON = os.path.join(DATA_PATH, 'twitter_timeline.json')


def test_twitter_timeline_xpath():
    with open(TWITTER_TIMELINE_JSON) as f:
        data = json.load(f)
    assert 'items_html' in data.keys()
    items_html = data['items_html']
    node = html.fromstring(items_html)
    tweet_nodes = node.xpath(TWEET_NODES_XPATH)

    for tweet_node in tweet_nodes:
        images = tweet_node.xpath(TWEET_PHOTO_XPATH)
        assert len(images) == 1
        assert images[0].startswith('https://')
        assert images[0].endswith(('.jpg', '.jpeg', '.png'))
        text = tweet_node.xpath(TWEET_TEXT_XPATH)
        assert text

    tweets = list(map(lambda node: { 'photo': node.xpath(TWEET_PHOTO_XPATH)[0],
                                    'caption': node.xpath(TWEET_TEXT_XPATH)[0] },
                      tweet_nodes))
    filterred_tweets = list(
        filter(lambda x: '月曜日のたわわ' in x['caption'], tweets)
    )
    assert len(tweets) == 20    # Twtter API length
    assert len(filterred_tweets) <= len(tweets)

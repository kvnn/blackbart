from bs4 import BeautifulSoup
from time import sleep
import praw
import os


def get_r():
    r = praw.Reddit(os.environ.get('REDDIT_BITCOIN_DEV_UA'))
    r.login(os.environ.get('REDDIT_BITCOIN_DEV_USERNAME'), os.environ.get('REDDIT_BITCOIN_DEV_PW'))
    return r


def handle_ratelimit(headers):
    if 'X-Ratelimit-Remaining' in headers:
        sleep(60)
    else:
        sleep(2)


def format_body(msg, show_time=False):
    body = BeautifulSoup(msg.body, 'html.parser')
    truncated_msg = '...[message truncated here by reddit bot]...'
    if show_time:
        date = msg.date.strftime('%b %d %Y %I:%M:%S%p')
    else:
        date = msg.date.strftime('%b %d %Y')
    for a in body.find_all('a'):
        markup = '[%s](%s)' % (a.text, a.attrs['href'])
        a.replaceWith(markup)
    body = body.text.replace('\n', '\n\n')
    body = '**%s** on %s:\n\n%s' % (msg.author_name, date, body)
    postfix = '\n\n------------\n\noriginal: [%s](%s)' % (msg.url, msg.url)
    if len(body) + len(postfix) > 10000:
        # reddit limit
        body = body[:10000 - len(body) - len(postfix) - len(truncated_msg)]
        body += truncated_msg
    body += postfix
    return body

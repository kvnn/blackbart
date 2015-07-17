import os

from django.core.management.base import BaseCommand

from blackbart.apps.distributor.models import SubredditSubmission
from blackbart.apps.miner.models import Message
from ..utils import format_body, handle_ratelimit, get_r


class Command(BaseCommand):
    '''Post any new submissions to reddit'''
    def _format_title(self, msg):
        date = msg.date.strftime('%b %d %Y')
        return '%s | %s | %s' % (msg.title, msg.author_name, date)

    def handle(self, *args, **options):
        sr = os.environ.get('REDDIT_BITCOIN_DEV_SUBREDDIT')
        r = get_r()
        for msg in Message.get_new_top_level_messages():
            handle_ratelimit(r.http.headers)
            post = r.submit(sr, self._format_title(msg), text=format_body(msg))
            SubredditSubmission.objects.create(
                message=msg,
                reddit_id=post.id,
                reddit_url=post.permalink,
                subreddit_name=sr
            )
            print 'posted %s' % post.permalink

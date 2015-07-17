from django.core.management.base import BaseCommand

from blackbart.apps.distributor.models import SubredditSubmission, SubredditComment
from ..utils import format_body, handle_ratelimit, get_r


class Command(BaseCommand):
    '''Post any new comments to each reddit submission'''
    def handle(self, *args, **options):
        r = get_r()
        submissions = SubredditSubmission.objects.all()
        for sub in submissions:
            comments = sub.get_new_comments()
            for msg in comments:
                handle_ratelimit(r.http.headers)
                reddit_sub = r.get_submission(submission_id=sub.reddit_id)
                post = reddit_sub.add_comment(format_body(msg, True))
                SubredditComment.objects.create(
                    submission=sub,
                    message=msg,
                    reddit_id=post.id,
                    reddit_url=post.permalink
                )
                print 'posted %s' % post.permalink

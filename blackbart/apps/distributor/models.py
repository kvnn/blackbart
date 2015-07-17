from django.db import models

from blackbart.apps.miner.models import Message


class SubredditSubmission(models.Model):
    reddit_id = models.CharField(max_length=255, unique=True)
    reddit_url = models.URLField(max_length=255, unique=True)
    subreddit_name = models.CharField(max_length=255)
    message = models.OneToOneField(Message)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_comments(self):
        '''Return Messages that should be treated as a comment to this Submission'''
        return Message.objects.filter(title=self.message.title)\
                              .exclude(id=self.message_id)\
                              .order_by('date')

    def get_new_comments(self):
        '''Return messages that should be treated as a comment to this Submission,
        and that do not have a SubredditComment object created for them'''
        return self.get_comments().filter(subredditcomment__isnull=True)


class SubredditComment(models.Model):
    reddit_id = models.CharField(max_length=255, unique=True)
    reddit_url = models.URLField(max_length=255, unique=True)
    message = models.OneToOneField(Message)
    submission = models.ForeignKey(SubredditSubmission)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


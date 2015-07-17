from django.db import models
from django.conf import settings


class Message(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    url = models.URLField(max_length=255, unique=True)
    scraped_url = models.URLField(max_length=255)
    author_name = models.CharField(max_length=255)
    author_email = models.CharField(max_length=255)
    body = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)
    parent_url = models.URLField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @classmethod
    def get_existing_urls_as_regex(cls):
        '''Return a list of urls for all Messages already scraped in regex'''
        return [tpl[0].split('/')[-1] for tpl in Message.objects.values_list('url')]

    @classmethod
    def get_top_level_messages(cls):
        '''Return a Message that was created first for each Message title'''
        min_date = '%s-01-01' % settings.MIN_YEAR
        q = '''SELECT m.* FROM miner_message m
                INNER JOIN
               (SELECT title, MIN(date) AS MinDate FROM miner_message GROUP BY title) grpmsgs
               ON m.title = grpmsgs.title AND m.date = grpmsgs.MinDate
               WHERE m.date >= '%s'
               ORDER BY m.date ASC''' % min_date
        return cls.objects.raw(q)

    @classmethod
    def get_new_top_level_messages(cls):
        '''Return a Message that was created first for each Message title,
        that has not been submitted to Reddit'''
        min_date = '%s-01-01' % settings.MIN_YEAR
        q = '''SELECT m.* FROM miner_message m
               LEFT JOIN distributor_subredditsubmission ss
                ON m.id = ss.message_id
               INNER JOIN
                (SELECT title, MIN(date) AS MinDate FROM miner_message GROUP BY title) grpmsgs
                ON m.title = grpmsgs.title AND m.date = grpmsgs.MinDate
               WHERE m.date >= '%s' AND ss.message_id IS NULL
               ORDER BY m.date ASC''' % min_date
        return cls.objects.raw(q)

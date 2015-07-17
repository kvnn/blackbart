from django.conf import settings
from django.core.management.base import BaseCommand

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals

from blackbart.apps.miner.scraper.spiders import LinuxFoundationSpider


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--year',
                            dest='year',
                            default=None,
                            help='Include to scrape messages from a specific year only')

    def handle(self, *args, **options):
        self.stdout.write('Start')
        spider = LinuxFoundationSpider(year=options.get('year'))
        crawler = Crawler(spider, settings.SPIDER_SETTINGS)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)

        crawler.crawl()
        reactor.run()  # the script will block here until the spider_closed signal is sent'''

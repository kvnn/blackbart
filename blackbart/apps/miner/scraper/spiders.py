# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from django.conf import settings

from .items import MessageItem
from ..models import Message


def remove_bad_prefixes(title):
    # TODO: Its possible for this to return None, which is bad, e.g. for title
    # '[Bitcoin-development][bitcoin-dev] [Bitcoin-development]Why not Child-Pays-For-Parent?'
    bads = ['[bitcoin-dev]',
            '[Bitcoin-development]',
            'Fwd:', 'Re:', '[Bulk]']
    for bad in bads:
        if bad in title and title.strip().index(bad) == 0:
            title = title[len(bad):].strip()
            return remove_bad_prefixes(title)
    return title


class LinuxFoundationSpider(CrawlSpider):
    name = "linuxfoundation_spider"
    allowed_domains = settings.LINUX_FOUNDATION_DOMAINS
    start_urls = settings.LINUX_FOUNDATION_URLS

    rules = (
        Rule(LinkExtractor(allow=('%s.*?(\\/date\\.html)' % settings.MIN_YEAR,))),
        Rule(LinkExtractor(restrict_xpaths=('//ul[2]/li/a[1]'), deny=Message.get_existing_urls_as_regex()),
             callback='parse_entry',
             follow=False,
        )
    )

    def _get_title(self, response):
        title = response.xpath('//h1[1]/text()').extract()[0]
        title = title.replace('\t', ' ').strip()
        new_title = remove_bad_prefixes(title)
        if new_title:
            return new_title
        return title

    def parse_entry(self, response):
        item = MessageItem()
        date = response.xpath('//i[1]/text()').extract()[0].strip()
        date = datetime.strptime(date, '%a %b %d %H:%M:%S %Z %Y')
        item['date'] = date
        item['title'] = self._get_title(response)
        item['author_name'] = response.xpath('//b[1]/text()').extract()[0].strip()
        item['author_email'] = response.xpath('//a[1]/text()').extract()[0].strip()
        previous_url = response.xpath('//ul[1]/li[text()="Previous message: "]//@href').extract()
        if len(previous_url):
            previous_url = previous_url[0]
            item['parent_url'] = '%s%s' % (response.url.split(response.url.split('/')[-1])[0], previous_url)
        item['body'] = ''.join(response.xpath('//pre[1]/node()').extract())
        item['scraped_url'] = response.url
        item['url'] = response.url
        yield item

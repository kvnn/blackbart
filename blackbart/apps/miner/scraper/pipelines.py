from scrapy.exceptions import DropItem

from ..models import Message


class MessagePipeline(object):
    def process_item(self, item, spider):
        if not Message.objects.filter(url=item['url']).exists():
            Message.objects.create(**item)
            return item
        raise DropItem()

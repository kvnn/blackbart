from scrapy.item import Item, Field


class MessageItem(Item):
    title = Field()
    date = Field()
    url = Field()
    author_name = Field()
    author_email = Field()
    body = Field()
    scraped_url = Field()
    parent_url = Field()

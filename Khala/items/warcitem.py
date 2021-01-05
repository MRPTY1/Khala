import scrapy


class WarcItem(scrapy.Item):
    url = scrapy.Field()
    headers = scrapy.Field()
    content = scrapy.Field()

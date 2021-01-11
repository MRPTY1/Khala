import scrapy


class HtmlItem(scrapy.Item):
    url = scrapy.Field()
    headers = scrapy.Field()
    text = scrapy.Field()

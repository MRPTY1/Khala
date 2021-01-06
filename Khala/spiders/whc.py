import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Khala.items.warcitem import WarcItem


class WhcSpider(CrawlSpider):
    name = 'whc'
    allowed_domains = ['whc.unesco.org']
    start_urls = ['https://whc.unesco.org/']
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    custom_settings = {
        # 爬取深度
        'DEPTH_LIMIT': 10,
        # 'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'Khala.middlewares.v2raynmiddleware.V2rayNMiddleware': 543
        },
        'ITEM_PIPELINES': {
            'Khala.piplines.warcpiplines.WarcWriterPipeline': 300,
        }
    }

    def parse_item(self, response):
        item = WarcItem()
        item['url'] = response.url
        item['headers'] = self.convert(response.headers)
        item['content'] = response.body
        yield item

    def convert(self, data):
        if isinstance(data, bytes):
            return data.decode('ascii')
        if isinstance(data, list):
            return data.pop().decode('ascii')
        if isinstance(data, dict):
            return dict(map(self.convert, data.items()))
        if isinstance(data, tuple):
            return map(self.convert, data)
        return data

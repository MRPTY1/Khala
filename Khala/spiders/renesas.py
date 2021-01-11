import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Khala.items.warcitem import WarcItem


class RenesasSpider(CrawlSpider):
    name = 'renesas'
    allowed_domains = ['renesas.com']
    start_urls = ['https://www.renesas.com/us/zh']
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    custom_settings = {
        # 日志输出目录
        # 'LOG_FILE': f'D:/ScrapyLog/{name}_log.txt',
        # 爬取深度
        'DEPTH_LIMIT': 10,
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOADER_MIDDLEWARES': {
            'Khala.middlewares.proxiesmiddleware.ProxiesMiddleware': 543
        },
        'ITEM_PIPELINES': {
            'Khala.pipelines.warcpipelines.WarcWriterPipeline': 300,
        }
    }

    def parse_item(self, response):
        item = WarcItem()
        item['url'] = response.url
        item['headers'] = self.convert(response.headers)
        item['content'] = response.body
        return item

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

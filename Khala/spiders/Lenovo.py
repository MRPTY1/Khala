import scrapy
from scrapy.http.response.html import HtmlResponse
import re
from urllib.parse import urlencode
from Khala.items.warcitem import WarcItem


class LenovoSpider(scrapy.Spider):
    name = 'Lenovo'
    start_urls = ['https://pcsupport.lenovo.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOADER_MIDDLEWARES': {
            'Khala.middlewares.proxiesmiddleware.ProxiesMiddleware': 543
        },
        'ITEM_PIPELINES': {
            'Khala.piplines.warcpiplines.WarcWriterPipeline': 300,
        }
    }

    def parse(self, response: HtmlResponse, **kwargs):
        url = 'https://pcsupport.lenovo.com/us/zh/products/'
        with open('Khala/lenovo/lenovo.txt', 'r+') as model_list:
            for model in model_list:
                model = model.replace('\n', '')
                yield response.follow(url=url + model, callback=self.follow_index, meta={'model': model})

    def follow_index(self, response: HtmlResponse):
        meta = response.meta
        url = 'https://pcsupport.lenovo.com/us/zh/api/v4/contents/productcontentslist'
        params = {
            "pids": "",
            "top": "0",
            "types": "MSH,KB,Forum.KB,TS,PS,LPDT",
            "countries": "us",
            "language": "zh"
        }
        text = response.text
        try:
            Guid = re.search(r'(?<=Guid":").*?(?=")', text).group(0)
            ParentGuids = re.search(r'(?<=ParentGuids":\[").*?(?="])', text).group(0).replace('"', '')
        except AttributeError:
            return
        params['pids'] = Guid + ',' + ParentGuids
        yield response.follow(url=url + '?' + urlencode(params), callback=self.get_contents_list, meta=meta)

    def get_contents_list(self, response: HtmlResponse):
        meat = response.meta
        contents_list = response.json().get('list')
        with open('Khala/lenovo/language.txt', 'r+') as languages:
            for language in languages:
                language = language.replace('\n', '')
                for contents in contents_list:
                    url = f'https://pcsupport.lenovo.com/us/{language}/products/{meat["model"]}/solutions/{contents["docid"]}'
                    yield response.follow(url=url, callback=self.out_item)

    def out_item(self, response):
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

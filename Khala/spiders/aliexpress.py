import scrapy
import json
from scrapy.http.response.html import HtmlResponse
from urllib.parse import urlencode
import re
from urllib.parse import urlsplit


class AliexpressSpider(scrapy.Spider):
    name = 'aliexpress'
    start_urls = ['https://www.aliexpress.com/']
    custom_settings = {
        'CONCURRENT_REQUESTS': 6,
        'AUTOTHROTTLE_ENABLED': True,
        "COOKIES_ENABLED": False,
        'LOG_LEVEL': 'DEBUG',
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'Khala.middlewares.v2raynmiddleware.V2rayNMiddleware': 543
        # }
    }
    languages = ['www.aliexpress.com', 'pt.aliexpress.com', 'es.aliexpress.com', 'fr.aliexpress.com',
                 'pl.aliexpress.com', 'he.aliexpress.com', 'it.aliexpress.com', 'tr.aliexpress.com',
                 'ko.aliexpress.com', 'ar.aliexpress.com']

    def parse(self, response: HtmlResponse, **kwargs):
        params = {
            "trafficChannel": "main",
            "catName": "t-shirts",
            "CatId": "100003127",
            "ltype": "wholesale",
            "SortType": "default",
            "page": "1"
        }
        with open('Khala/spider_params/aliexpress/categories.json', 'r') as file:
            categories = json.loads(file.read())
            for k, v in categories.items():
                url = f'https://www.aliexpress.com/category/{k}/{v}.html'
                params['CatId'] = k
                params['catName'] = v
                for page in range(1, 61):
                    params['page'] = str(page)
                    yield response.follow(url=url + '?' + urlencode(params), callback=self.get_list)

    def get_list(self, response: HtmlResponse):
        for url in re.findall(r'(?<=productDetailUrl":"//).*?(?=")', response.text):
            for language in self.languages:
                yield response.follow(url=re.sub(r'www.*?com', 'https://' + language, url),
                                      callback=self.get_item)

    def get_item(self, response: HtmlResponse):
        url = urlsplit(response.url)
        title = re.search(r'(?<="subject":").*?(?=")', response.text)
        if title:
            title = title.group(0)
        item = {
            'netloc': url.netloc,
            'path': url.path,
            'title': title
        }
        return item

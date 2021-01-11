import re
import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse
from Khala.tools.get_date import get_date
from urllib.parse import urlencode
from Khala.items.htmlitem import HtmlItem


class GovSpider(scrapy.Spider):
    name = 'gov'
    start_urls = ['https://sc.news.gov.hk/TuniS//www.news.gov.hk/chi/index.html']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'Khala.middlewares.v2raynmiddleware.V2rayNMiddleware': 543
        },
        'ITEM_PIPELINES': {
            'Khala.pipelines.mongopipelines.MongoPipeline': 300,
        }
    }

    def parse(self, response: HtmlResponse, **kwargs):
        url = 'https://www.news.gov.hk/jsp/NewsArticle.jsp'
        new_url = 'https://sc.news.gov.hk/TuniS/www.news.gov.hk/jsp/NewsArticle.jsp'
        category_list = ['finance', 'school_work', 'health', 'environment', 'law_order', 'infrastructure', 'admin',
                         'city_life', 'record']
        language_list = ['eng', 'chi']
        params = {
            'language': 'chi',
            'category': 'finance',
            'date': '',
        }
        for date in get_date():
            for category in category_list:
                if date == '202102':
                    break
                for language in language_list:
                    params['date'] = date
                    params['language'] = language
                    params['category'] = category
                    yield response.follow(url=url + '?' + urlencode(params), callback=self.get_news_list)
                params['language'] = 'chi'
                yield response.follow(url=new_url + '?' + urlencode(params), callback=self.get_news_list)

    def get_news_list(self, response: HtmlResponse):
        text = response.text
        url = 'https://www.news.gov.hk'
        if 'sc.news.gov.hk' in response.url:
            url = 'https://sc.news.gov.hk/TuniS/www.news.gov.hk'
        for path in re.findall(r'(?<=<generateHtmlPath>).*?(?=</generateHtmlPath>)', text):
            yield response.follow(url=url + path, callback=self.get_news)

    def get_news(self, response: HtmlResponse):
        if response.status == 404:
            return
        item = HtmlItem()
        item['url'] = response.url
        item['text'] = response.text
        return item

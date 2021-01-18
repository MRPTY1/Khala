import scrapy
from lxml import etree
from scrapy.http.response.html import HtmlResponse
import re


class ApcSpider(scrapy.Spider):
    name = 'apc'
    start_urls = ['https://www.apc.com/cn/zh/download/search-by-current-and-legacy-product/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'Khala.pipelines.mongopipelines.MongoPipeline': 300,
        }
    }

    def parse(self, response: HtmlResponse, **kwargs):
        text = response.text
        html = etree.HTML(text)
        for html_href in html.xpath("//div[@class='letterBox clearfix']//a/@href"):
            yield response.follow(url=html_href + '?langFilterDisabled=true', callback=self.get_count)

    def get_count(self, response: HtmlResponse):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        html = etree.HTML(response.text)
        count = int(html.xpath('string(//span[@id="documentCount"])'))
        url = re.sub(r'\?.*', 'resultViewCahnge/resultListAjax', response.url)
        for i in range(1, int(count / 50) + 2):
            data = 'data=langFilterDisabled%3Dtrue_COMMA_sortByField%3DRelevance_COMMA_' \
                   f'pageNumber%3D{i}_COMMA_itemsPerPage%3D50'
            yield response.follow(headers=headers, url=url, method='post', body=data, callback=self.get_pdf_list)

    def get_pdf_list(self, response: HtmlResponse):
        for data in response.json().get('docList'):
            if data.get('downloadUrl'):
                bson = {'url': data['downloadUrl']}
                yield bson

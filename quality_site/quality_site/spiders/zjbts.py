# -*- coding: utf-8 -*-
import scrapy
from quality_site.items import ZjbtsNewsItem
from quality_site.itemloaders import NewsLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
import json
from hashlib import sha1
from scrapy.utils.python import to_bytes


class ZjbtsSpider(scrapy.Spider):
    name = 'zjbts'

    pipeline = ['BaseUniqueItemPersistencePipeline', 'DownloadFilePipeline']

    allowed_domains = ['http://www.zjbts.gov.cn']
    request_list_url = 'http://www.zjbts.gov.cn/DoAjax.ashx?Flag=getmobilelist&tableCode=cctg&page={page}'

    def get_thread_from_url(self, url):
        return url.split('/')[-1].split('.')[0]

    def start_requests(self):
        pages = int(getattr(self, 'pages', 1))

        for page in range(pages):
            yield scrapy.Request(url=self.request_list_url.format(page=str(page)),
                                 callback=self.parse_list,
                                 dont_filter=True)

    def parse_list(self, response):

        html = response.body.decode(response.encoding)
        html = html.replace('title', '"title"')
        html = html.replace('newspath', '"newspath"')
        html = html.replace('%', '\\\\')

        html = '{"list":' + html + '}'
        news_list = json.loads(html)['list']

        for news in news_list:
            title = news['title'].encode('utf-8').decode('unicode_escape')
            path = news['newspath']
            href = 'http://www.zjbts.gov.cn/' + path
            yield scrapy.Request(url=href,
                                 dont_filter=True,
                                 callback=self.parse_detail)


    def add_domain(self,x):
        file_url = 'http://www.zjbts.gov.cn' + x
        return file_url

    def extract_file_name(self,x):
        return x.split('：')[-1].replace('\n', '')

    def parse_detail(self, response):

        news_loader = NewsLoader(item=ZjbtsNewsItem(), response=response)

        news_loader.add_value('thread', self.get_thread_from_url(response.url))
        news_loader.add_value('source_link', response.url)

        news_loader.add_xpath('title', '//div[@class="newsTitle"]')

        # news_loader.add_xpath('created', '//div[@class="publish"]/text()')
        # news_loader.add_xpath('created', '//div[@class="info"]/text()')
        # news_loader.add_xpath('author', '//div[@class="publish"]/span[@class="from"]')
        news_loader.add_xpath('author_and_date', '//div[@class="newsAttr"]')

        news_loader.add_xpath('raw_content', '//div[@class="newsContent"]')
        news_loader.add_xpath('content', '//div[@class="newsContent"]//text()')
        news_loader.add_xpath('file_urls', '//div[@class="newsContent"]//a/@href', MapCompose(self.add_domain))
        news_loader.add_xpath('file_name', '//div[@class="newsContent"]//a/text()', MapCompose(self.extract_file_name))

        news = news_loader.load_item()

        yield news



# -*- coding: utf-8 -*-
import scrapy
from quality_site.items import QualityNewsItem
from quality_site.itemloaders import NewsLoader


class CqnSpider(scrapy.Spider):
    name = 'cqn'

    pipeline = ['LocationPipeline', 'BaseUniqueItemPersistencePipeline']

    allowed_domains = ['http://www.cqn.com.cn']
    request_list_url = 'http://www.cqn.com.cn/search/servlet/SearchServlet.do?contentKey={keyword}&sort=date&op=single&pageNo={page}'

    def get_thread_from_url(self, url):
        return url.split('_')[-1].split('.')[0]

    def start_requests(self):
        keyword = getattr(self, 'keyword', None)
        pages = int(getattr(self, 'pages', 1))
        if keyword is None:
            return

        for page in range(1, pages + 1):
            yield scrapy.Request(url=self.request_list_url.format(page=str(page), keyword=keyword),
                                 callback=self.parse_list,
                                 dont_filter=True)

    def parse_list(self, response):
        for info in response.xpath('//tr[@class="TableBody1"]'):
            href = info.xpath('.//div[@class="jsg1"]/a/@href').extract_first()
            summary = info.xpath('string(.//div[@class="jsg2"])').extract_first()

            yield scrapy.Request(url=href,
                                 dont_filter=True,
                                 meta={'summary': summary},
                                 callback=self.parse_detail)

    def parse_detail(self, response):

        news_loader = NewsLoader(item=QualityNewsItem(), response=response)
        news_loader.add_value('category', getattr(self, 'category', getattr(self, 'keyword', None)))
        news_loader.add_value('thread', self.get_thread_from_url(response.url))
        news_loader.add_value('source_link', response.url)
        news_loader.add_xpath('source_name', '//meta[@name="Author"]/@content')
        news_loader.add_xpath('keywords', '//meta[@name="KeyWords"]/@content')
        news_loader.add_value('summary', response.meta['summary'])
        #
        news_loader.add_xpath('title', '//div[@class="Detail_Title"]/h1/text()')
        news_loader.add_xpath('title', '//div[@class="title"]/text()')
        news_loader.add_xpath('create_date', '//div[@class="publish"]/text()')
        news_loader.add_xpath('create_date', '//div[@class="info"]/text()')
        news_loader.add_xpath('author', '//div[@class="publish"]/span[@class="from"]')
        news_loader.add_xpath('author', '//div[@class="info"]/span/text()')

        news_loader.add_xpath('raw_content', '//div[@class="content"]')
        news_loader.add_xpath('content', '//div[@class="content"]//text()')
        news_loader.add_xpath('image_url', '//div[@class="content"]//img/@src')

        news = news_loader.load_item()

        if 'title' in news:
            return news

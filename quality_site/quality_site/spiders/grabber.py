# -*- coding: utf-8 -*-

import scrapy
from quality_site.items import FileDownloadItem

# For model support.
from quality_site.items import ZjbtsNewsItem
from stems.models import QualityNews, ZjbtsNews

from hashlib import sha1


####################################################################################
#                                                                                  #
# USAGE: nohup scrapy crawl grabber -a from_id=1 -a to_id=1 -a category=exposure \ #
#        -a model=BaoguangItem -a field=image_url --loglevel=INFO --logfile=log &  #
#                                                                                  #
####################################################################################

class GrabberSpider(scrapy.Spider):
    name = 'grabber'
    pipeline = ['DownloadFilesPipeline']
    allowed_domains = ['http://www.zjbts.gov.cn']
    #NOTE: (zacky, 2015.JUN.2nd) FAKE URL TO PROCESS SUCCESSFULLY.
    fake_url = 'https://www.cc98.org/'
    start_urls = []

    # DOWNLOAD_DELAY=6
    # custom_settings = {"DOWNLOAD_DELAY": 0.5}


    def __init__(self, from_id=None, to_id=None, category='Xjd', model='ZjbtsNews', field='file_urls', *args, **kwargs):
        self.logger.debug(locals())
        self.model = model

        self.category = category
        self.field = field
        self.queue = []
        super(GrabberSpider, self).__init__(*args, **kwargs)

    def start_requests(self):

        for obj in eval(self.model).objects.all():
            if not obj:
                continue
            urls = getattr(obj, self.field)
            if not urls:
                continue

            self.queue.append((urls, obj.file_name))
            # img_grabber_executed = getattr(obj, "img_grabber_executed")
            # if img_grabber_executed:
            #     continue
            # setattr(obj, "img_grabber_executed", True)
            # obj.save()

        yield self.make_requests_from_url(self.fake_url)
    #
    def parse(self, response):


        # urls = [urls for urls, file_name in self.queue]
        # item = FileDownloadItem()
        # item['file_name'] = file_name
        # item['file_urls'] = urls
        # yield item

        for urls, file_name in self.queue:
            item = FileDownloadItem()
            item['file_name'] = file_name
            item['file_urls'] = urls
            yield item

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

from base.items import BaseItem
from stems.models import QualityNews, ZjbtsNews


class QualityNewsItem(BaseItem):
    django_model = QualityNews
    update_fields_list = ['source_name', 'source_link', 'title', 'location', 'create_date', 'author', 'view_count',
                          'summary', 'content', 'raw_content', 'image_url', 'keywords']
    unique_key = ('thread', 'category')



class ZjbtsNewsItem(BaseItem):
    django_model = ZjbtsNews
    update_fields_list = ['source_link', 'title', 'author_and_date', 'content', 'raw_content', 'file_urls', 'file_name']
    unique_key = ('thread',)

class FileDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    file_urls=scrapy.Field()
    file_name=scrapy.Field()

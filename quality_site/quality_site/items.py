# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from base.items import BaseItem
from stems.models import QualityNews


class QualityNewsItem(BaseItem):
    django_model = QualityNews
    update_fields_list = ['source', 'link', 'title', 'location', 'created', 'author', 'view_cnt',
                          'summary', 'content', 'raw_content', 'image_url', 'keywords']
    unique_key = ('thread', 'category')

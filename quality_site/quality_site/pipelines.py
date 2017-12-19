# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from base.pipelines import BaseUniqueItemPersistencePipeline, check_spider_pipeline
from quality_site.items import QualityNewsItem


class AddressPipeline(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
        if isinstance(item, QualityNewsItem):
            if '浙江' in item['content'] or '浙江' in item['title']:
                item['address'] = '浙江'
            else:
                item['address'] = '未知'

        return item

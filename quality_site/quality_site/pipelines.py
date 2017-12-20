# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from base.pipelines import BaseUniqueItemPersistencePipeline, check_spider_pipeline
from quality_site.items import QualityNewsItem
import json


class LocationPipeline(object):
    def open_spider(self, spider):
        self.locations = json.load(open('quality_site/location.json'))

    @check_spider_pipeline
    def process_item(self, item, spider):
        if isinstance(item, QualityNewsItem):
            item['location'] = dict()
            for province in self.locations:
                if province['name'] in item['title'] or province['name'] in item['content']:
                    city_list = list()
                    for city in province['city'][:-1]:
                        if city['name'] != '其他' and (city['name'] in item['title'] or city['name'] in item['content']):
                            city_list.append(city['name'])
                    if province['name'] in item['location']:
                        item['location'][province['name']].append(city_list)
                    else:
                        item['location'][province['name']] = city_list

            for province in self.locations:
                for city in province['city'][:-1]:
                    if city['name'] != '其他' and (city['name'] in item['title'] or city['name'] in item['content']):
                        if province['name'] in item['location'] and city['name'] not in item['location'][
                            province['name']]:
                            item['location'][province['name']].append(city['name'])
                        else:
                            item['location'][province['name']] = [city['name'], ]

        return item

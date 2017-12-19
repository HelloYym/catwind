# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
from w3lib.html import remove_tags


def get_trunk(content):
    content = content.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').strip()
    if content != '': return content


def filter_word(x):
    return None if x == 'world' else x


def skip_first(values, num):
    return values[num:]


class NewsLoader(ItemLoader):
    default_input_processor = MapCompose(get_trunk, remove_tags)
    default_output_processor = TakeFirst()

    created_in = MapCompose(str.strip)

    content_out = Join('')

    raw_content_in = MapCompose(get_trunk)
    raw_content_out = Join('')

    image_url_out = Join('#')

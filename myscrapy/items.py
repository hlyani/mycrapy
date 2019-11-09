# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    diamond = scrapy.Field()
    last_order = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    level = scrapy.Field()
    recommend = scrapy.Field()
    commend_people = scrapy.Field()
    commend = scrapy.Field()
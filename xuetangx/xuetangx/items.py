# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XuetangxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    instructors = scrapy.Field()
    description = scrapy.Field()
    long_intro = scrapy.Field()
    teachers = scrapy.Field()
    curriculum = scrapy.Field()

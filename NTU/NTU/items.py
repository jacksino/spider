# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NtuItem(scrapy.Item):
    name = scrapy.Field()
    teacher = scrapy.Field()
    summary = scrapy.Field()
    traget = scrapy.Field()
    requirment = scrapy.Field()
    test = scrapy.Field()

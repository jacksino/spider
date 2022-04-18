# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EdxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    slug = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    video = scrapy.Field()
    abstract = scrapy.Field()
    fullDescription = scrapy.Field()
    enrollmentCount = scrapy.Field()
    key = scrapy.Field()
    levelType = scrapy.Field()
    outcome = scrapy.Field()
    syllabusRaw = scrapy.Field()
    entitlements = scrapy.Field()
    offered_by = scrapy.Field()

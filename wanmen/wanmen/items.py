# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WanmenItem(scrapy.Item):
    title=scrapy.Field()
    description=scrapy.Field()
    lightSpots=scrapy.Field()
    suitable=scrapy.Field()
    obtains=scrapy.Field()
    teachers=scrapy.Field()
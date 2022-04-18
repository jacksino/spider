# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocItem(scrapy.Item):
   topic = scrapy.Field()
   title = scrapy.Field()
   url = scrapy.Field()
   arrange = scrapy.Field()
   start_time = scrapy.Field()
   hours_arrange =scrapy.Field()
   full_description =scrapy.Field()
   aim = scrapy.Field()
   outline =scrapy.Field()
   need = scrapy.Field()
   graduation = scrapy.Field()
   reference = scrapy.Field()


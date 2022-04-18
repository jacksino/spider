# -*- coding: utf-8 -*-
import codecs,json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MoocPipeline(object):
    def process_item(self, item, spider):
        return item
import codecs,json


class JsonCreatePipeline(object):
    def __init__(self):
        self.file = codecs.open('spiderdata.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

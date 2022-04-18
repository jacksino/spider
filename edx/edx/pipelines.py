# -*- coding: utf-8 -*-
import json
from .settings import PATH
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class EdxPipeline(object):

    def __init__(self):
        self.file = open(PATH+"/courses.txt", "w+", encoding="utf-8")

    def process_item(self, item, spider):
        data = json.dumps(dict(item))
        self.file.write(data)
        self.file.write("\n")
        return item["slug"]

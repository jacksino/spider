# -*- coding: utf-8 -*-
import os
import json
from .settings import SAVE_PATH

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MitPipeline(object):

    def __init__(self):
        path = os.path.join(SAVE_PATH, "courses.txt")
        self.file = open(path, "w+", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item)))
        self.file.write("\n")
        return item.get("title")

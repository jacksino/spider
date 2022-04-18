# -*- coding: utf-8 -*-
import os
import json
from .settings import SAVE_PATH

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Study163Pipeline(object):
    def __init__(self):
        super().__init__()
        self.file = open(os.path.join(
            SAVE_PATH, "courses.txt"), "w+", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False))
        self.file.write("\n")
        return item.get("title")

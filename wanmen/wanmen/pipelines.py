import os,json
from .settings import PATH

class WanmenPipeline(object):
    def __init__(self):
        filepath = os.path.join(PATH, "courses.txt")
        self.file = open(filepath, "w+", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False))
        self.file.write("\n")
        return item.get("title")

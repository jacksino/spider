# -*- coding=utf-8 -*-
import os
import json
import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.http import JsonRequest

from ..items import XuetangxItem
from ..settings import SAVE_PATH


class XuetangxSpider(scrapy.Spider):
    name = "xuetangx"
    allowed_domains = ["xuetangx.com"]
    first_url = "https://next.xuetangx.com/api/v1/lms/get_product_list/?page=1"
    list_url = "https://next.xuetangx.com/api/v1/lms/get_product_list/?page={}"
    detail_url = "https://next.xuetangx.com/api/v1/lms/product/get_course_detail/?cid={}"
    max_page = None

    def __init__(self):
        path = os.path.join(SAVE_PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield JsonRequest(self.first_url, method="POST", body=json.dumps(self.make_payload()), callback=self.parse_first)

    def parse_first(self, response: Response):
        data = json.loads(response.text)
        data = data.get("data", None)
        if not data:
            return

        count = data.get("count", None)
        if not count:
            return
        self.max_page = count//10+(1 if count % 10 > 0 else 0)

        for i in range(self.max_page):
            yield JsonRequest(self.list_url.format(i+1), method="POST", body=json.dumps(self.make_payload()), callback=self.parse_list)

    def parse_list(self, response: Response):
        data = json.loads(response.text)
        data = data.get("data", None)
        if not data:
            return

        product_list = data.get("product_list", [])
        for p in product_list:
            cid = p.get("classroom_id", [])[-1]
            sign = p.get("sign", None)
            if cid and sign:
                url = "https://next.xuetangx.com/course/{}/{}".format(
                    sign, cid)
                yield Request(self.detail_url.format(cid), callback=self.parse_detail, meta={"url": url})
                yield Request(url, callback=self.parse_html)

    def parse_detail(self, response: Response):
        data = json.loads(response.text)
        data = data.get("data", None)
        if not data:
            return

        item = XuetangxItem()
        basic_data = data.get("basic_data", None)
        if basic_data:
            item["title"] = basic_data.get("name", "")
            item["url"] = response.meta.get("url", "")
            item["instructors"] = basic_data.get("short_intro", "")
            item["description"] = basic_data.get("description", "")
            item["long_intro"] = basic_data.get("long_intro", "")
            item["teachers"] = basic_data.get("teacher_list", [])

        content_data = data.get("content_data", None)
        if content_data:
            item["curriculum"] = content_data
        else:
            item["curriculum"] = []
        yield item

    def parse_html(self, response: Response):
        filename = response.url.split("/")[-2]+".html"
        with open(os.path.join(SAVE_PATH, "html", filename), "w+", encoding="utf-8") as f:
            f.write(response.xpath("/html/body").extract()[0])
            f.close()

    def make_payload(self):
        ret = {
            "query": "",
            "chief_org": [],
            "classify": [],
            "selling_type": [],
            "status": [],
            "appid": 10000,
        }
        return ret

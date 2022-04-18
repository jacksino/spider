# -*- coding:utf-8 -*-
import os
import re
import time
import json
import scrapy
from scrapy import Request
from scrapy import FormRequest
from scrapy.http import Response

from ..settings import SAVE_PATH
from ..items import Study163Item


def generateTimeStamp():
    return int(round(time.time()*1000))


class Study163Crawler(scrapy.Spider):

    name = "study163"
    allowed_domains = ["163.com"]

    startUrl = "https://home.study.163.com/home/j/web/getFrontCategory.json?t={}"
    categroyUrl = "https://study.163.com/j/web/fetchPersonalData.json?categoryId={}&t={}"
    planUrl = "https://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?{}"

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)

        path = os.path.join(SAVE_PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield Request(
            url=self.startUrl.format(generateTimeStamp()),
            callback=self.parse_first
        )

    def parse_first(self, response: Response):
        data = json.loads(response.text)
        result = data.get("result", [])

        temp = []
        for r in result:
            temp.extend(r.get("children", []))
        children = []
        for i in temp:
            children.extend(i.get("children", []))
        ids = []
        for c in children:
            t = c.get("id", None)
            if t:
                ids.append(t)
        # print(ids)

        for i in ids:
            yield Request(
                url=self.categroyUrl.format(i, generateTimeStamp()),
                callback=self.parse_category
            )

    def parse_category(self, response: Response):
        data = json.loads(response.text)
        # print(data)
        result = data.get("result", [])
        if not result:
            return

        courses = []
        for r in result:
            if r.get("module", {}).get("moduleType") == 1:
                continue
            courses.extend(r.get("contentModuleVo", []))

        for c in courses:
            title = c.get("productName", "")
            url = "http:"+c.get("targetUrl", "")
            yield Request(url=url, callback=self.parse_course, meta={"title": title})

    def parse_course(self, response: Response):
        temp = response.request.headers.getlist("Cookie")[0]
        sessionId = re.findall(r"NTESSTUDYSI=(.*?);", temp.decode("utf-8"))
        payload = {
            "callCount": "1",
            "scriptSessionId": r"${scriptSessionId}190",
            "httpSessionId": sessionId,
            "c0-scriptName": "PlanNewBean",
            "c0-methodName": "getPlanCourseDetail",
            "c0-id": "0",
            "c0-param0": "string:1005084022",
            "c0-param1": "number:0",
            "c0-param2": "null:null",
            "batchId": str(generateTimeStamp())
        }

        # print(json.dumps(payload))
        yield FormRequest(
            url=self.planUrl.format(generateTimeStamp()),
            formdata=payload,
            meta=response.meta,
            callback=self.parse_info
        )

    def parse_info(self, response: Response):
        # print(response.text)
        temp = re.findall(r'description="(.*?)";', response.text)
        text = []
        for t in temp:
            text.append(t.encode("utf-8").decode("unicode_escape"))
        if not text:
            return

        item = Study163Item()
        item["title"] = response.meta.get("title", "")
        item["description"] = text[0]
        item["curriculum"] = ["{}.{}".format(
            i, t) for i, t in enumerate(text[1:])]

        yield item

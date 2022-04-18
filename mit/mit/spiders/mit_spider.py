# -*- coding=utf-8 -*-
import os
import time
import json
import scrapy
from scrapy import Request
from scrapy.http import Response

from ..settings import SAVE_PATH
from ..items import MitItem


def generate_time(url):
    timeStamp0 = round(time.time()*1000)
    timeStamp1 = round(time.time()*1000)+1
    return "{}?{}&_={}".format(url, timeStamp0, timeStamp1)


class MitSpider(scrapy.Spider):
    name = "mit"
    allowed_domains = [
        "mit.edu"
    ]

    url_base = "https://ocw.mit.edu"
    department_url = "https://ocw.mit.edu/courses/find-by-number/departments.json"
    courses_url = "https://ocw.mit.edu/courses/{}/index.json"

    def __init__(self):
        path = os.path.join(SAVE_PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield Request(generate_time(self.department_url), callback=self.parser_departments)

    def parser_departments(self, response: Response):
        data = json.loads(response.text)
        for item in data:
            url = self.courses_url.format(item.get("id", "#"))
            yield Request(generate_time(url), callback=self.parser_courses)

    def parser_courses(self, response: Response):
        data = json.loads(response.text)
        for item in data:
            url = self.url_base+item.get("href", "/#")
            yield Request(url, callback=self.parser_details)

    def parser_details(self, response: Response):
        filename = response.url.split("/")[-2]+".html"
        with open(SAVE_PATH+"/html/"+filename, "w+", encoding="utf-8") as f:
            f.write(response.xpath("/html/body").extract()[0])

        item = MitItem()
        data = response.xpath(
            '''//*[@id="course_title"]/h1/text()''').extract()
        item["title"] = data[0] if data else ""
        item["url"] = response.url
        data = response.xpath(
            '''//*[@id="course_info"]/p[1]/text()''').extract()
        item["instructors"] = data[0] if data else ""
        data = response.xpath(
            '''//*[@id="description"]/div/p/text()''').extract()
        item["description"] = data[0] if data else ""
        yield Request(response.url+"calendar/", callback=self.parser_curriculum, meta={"item": item})

    def parser_curriculum(self, response: Response):
        item = response.meta.get("item", MitItem())
        data = response.xpath(
            '''//*[@id="course_inner_section"]/div[1]/table''').extract()
        item["curriculum"] = data[0] if data else ""
        yield item

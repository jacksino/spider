import os
import json
import scrapy
import time
import re
from scrapy import Request
from scrapy.http import Response
from ..items import UdacityItem
from ..settings import PATH

from .find_text import *

class Udacity(scrapy.Spider):
    name = "udacity"
    allowed_domains = "*"
    start_url = "https://catalog-api.udacity.com/v1/catalog?locale=zh-cn"

    def __init__(self):
        path = os.path.join(PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield Request(self.start_url,callback=self.parse_detail,dont_filter=True)

    def parse_detail(self, response:Response):
        data = json.loads(response.text)
        courses = data.get("courses",None)
        for i in range(0,len(courses)):
            if courses:
                item = UdacityItem()
                course = courses[i]
                item["title"]=course.get("title",None)
                instructor = course.get("instructors",None)
                item["instructor"]= find_teachers(instructor)
                item["level"]=course.get("level",None)
                program_syllabus = course.get("program_syllabus",None)
                lesson = program_syllabus.get("lessons",None)
                item["lessons"]=find_lessons(lesson)
                item["selling_points"]=(course.get("summary",None))
                item["suitable"]=course.get("required_knowledge",None)
                slug = course.get("slug")
                course_url = "https://cn.udacity.com/course/{}".format(slug)
                yield Request(course_url,callback=self.parse_course,dont_filter=True,meta={'item': item})

    def parse_course(self, response:Response):
        item = response.meta.get("item",UdacityItem())
        item["price"]=response.xpath('//div[@class="section"]/div[1]/div/h5//text()').extract()
        item["learning_duration"]=response.xpath('//div[@class="section"]/div[2]/h5//text()').extract()
        filename = "{}.html".format(item["title"])
        with open(os.path.join(PATH, "html", filename), "w+", encoding="utf-8") as f:
            f.write(response.xpath("/html/body").extract()[0])
            f.close()
        yield item







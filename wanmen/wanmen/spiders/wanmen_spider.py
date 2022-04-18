import re
import os
import json
import scrapy
from scrapy import Request
from scrapy import FormRequest
from scrapy.http import Response
import js2py

from .text_get import find_text,find_teacher
from ..items import WanmenItem
from  ..settings import PATH

class Wanmen_pider(scrapy.Spider):
    name = "wanmen"
    allowed_domains = "*"
    start_url = "https://www.wanmen.org/uni/catalog"


    def __init__(self):
        path = os.path.join(PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield Request(self.start_url,callback=self.parse_page,dont_filter=True)

    #构造url，请求api接口
    def parse_page(self,response:Response):
        for i in range(1 ,35):
            current_path = os.path.dirname(__file__)
            with open(current_path + '/token.js', 'r+') as fp:
                js = fp.read()
                context = js2py.EvalJs()
                context.execute(js)
                token = context.token
                time = context.time

            headers = {
                'referer': 'https://www.wanmen.org/uni/catalog',
                'origin': 'https: // www.wanmen.org',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'x-token': token,
                'x-time': time,
                'content-type': 'application/x-www-form-urlencoded'
            }
            api_url = "https://api.wanmen.org/4.0/content/courses?limit=32&page={}".format(i)
            yield Request(api_url,headers=headers,callback=self.parse_detail,dont_filter=True)




    def parse_detail(self, response:Response):
        data = json.loads(response.text)
        item = WanmenItem()
        for i in range(0,32):
            para = data[i].get("seo", None)
            item["title"] = para.get("title", None)
            course_detail = data[i].get("details",None)
            if course_detail is None:
                return
            des = course_detail.get("imageTexts",None)
            context1 = des.get("context",None)
            item["description"] = find_text(context1)
            lightspots = course_detail.get("lightSpots",None)
            context2 = lightspots.get("context", None)
            item["lightSpots"] = find_text(context2)
            suit = course_detail.get("suitable",None)
            context3 = suit.get("context", None)
            item["suitable"] = find_text(context3)
            obtains = course_detail.get("obtains",None)
            context4 = obtains.get("context", None)
            item["obtains"] = find_text(context4)
            teachers = course_detail.get("teachers",None)
            context5 = teachers.get("context", None)
            item["teachers"] = find_teacher(context5)
            yield item









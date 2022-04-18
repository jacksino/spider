import re
import os
import json
import scrapy
from scrapy import Request
from scrapy import FormRequest
from scrapy.http import Response
from ..items import NtuItem
from ..settings import PATH


class NTUspider(scrapy.Spider):
    name = "NTU"
    allowed_domains = "ocw.aca.ntu.edu.tw"
    start_url = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/coupage/1"

    def __init__(self):
        path = os.path.join(PATH, "html")
        if not os.path.exists(path):
            os.makedirs(path)

    def start_requests(self):
        yield Request(self.start_url,callback=self.parse_first)

    def parse_first(self, response: Response):
        end = response.xpath('//ul[@class="pagecount"]/li[last()]/a/@href').extract()[0]
        res = re.findall("/ntu-ocw/ocw/coupage/(.*)",end,re.S)
        for i in range(1,int(res[0])+1):
            page_url = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/coupage/{}".format(i)
            yield Request(page_url,callback=self.parse_course,dont_filter=True)

    def parse_course(self, response: Response):
        course_urls = response.xpath('//div[@class="coursepic"]/a/@href').extract()
        for course_url in course_urls:
            if course_url:
                url = "http://ocw.aca.ntu.edu.tw/{}".format(course_url)
                res = re.findall("http://ocw.aca.ntu.edu.tw//ntu-ocw/index.php/ocw/cou/(.*)",url,re.S)
                intro_url = "http://ocw.aca.ntu.edu.tw/ntu-ocw/ocw/cou_intro/{}".format(res[0])
                yield Request(intro_url,callback=self.parse_detail,dont_filter=True)


    def parse_detail(self, response:Response):
        item = NtuItem()
        item["name"] = response.xpath('//h2[@class="title"]//text()').extract()
        item["teacher"] = response.xpath('//h4[@class="unit"]//text()').extract()
        item["summary"] = response.xpath('string(//h3[contains(text(),"課程概述")]/following-sibling::p[1])').extract()
        item["traget"] = response.xpath('string(//h3[contains(text(),"課程目標")]/following-sibling::p[1])').extract()
        item["test"] = response.xpath('string(//h3[contains(text(),"成績評量方式")]/following-sibling::p[1])').extract()
        item["requirment"] = response.xpath('string(//h3[contains(text(),"課程要求")]/following-sibling::p[1])').extract()
        filename = "{}.html".format(item["name"])
        with open(os.path.join(PATH, "html", filename), "w+", encoding="utf-8") as f:
            f.write(response.xpath("/html/body").extract()[0])
            f.close()
        yield item
import os
import json
import scrapy
from ..items import MoocItem
from ..settings import PATH
import codecs

class MoocSpider(scrapy.Spider):
    name = "mooc"
    allowed_domains = ['www.icourse163.com']
    start_urls = ['https://www.icourse163.org']


    def parse_root(self, response):
        item = MoocItem()
        courseDetails = response.xpath('//div[@class="u-cateItem-container"]')
        for courseDetail in courseDetails:
            item['topic'] = response.xpath('//div[@class="u-cateItem-container"]/@data-label').extract()
            topics_url = courseDetail.xpath('.//a/@href').extract()[0]
            yield scrapy.Request(url=topics_url,callback=self.parse_topics,meta={'item':item})

    def parse_topics(self,response):
        request_url = 'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc?csrfKey=b4bd55df16d2448fab22e053b8cfd56f'
        item=response.meta['item']
        ajaxParm = response.meta
        for pageIndex in range(1,ajaxParm['totlepageCount']+1):
            myFormData={
                "categoryId": -1,
                "categoryChannelId": ajaxParm['categoryChannelId'],
                "orderBy": 0,
                "stats": 30,
                "pageIndex": pageIndex,
                "pageSize": 20
            }
            yield scrapy.FormRequest(request_url,formdata=myFormData,callback=self.parse_html,meta={'item':item})

    def parse_html(self,response):
        item = response.meta['item']
        data = json.loads(response.text)
        if data is None:
            return
        content = data.get['result']
        if content is None:
            return
        course_list = content.get['list']
        if course_list is None:
            return
        for i in range[0,20]:
            course = course_list.get[i]
            course_id = course.get['id']
            course_scl = course.get['schoolSN']
            course_url = 'https://www.icourse163.org/course/'+course_scl+'-'+course_id
            item['url']=course_url
            yield scrapy.Request(course_url,meta={'item':item},callback=self.parse_course)

    def parse_course(self, response):
        item = response.meta['item']
        item['title']=response.xpath('//span[class = "course-title"]').extract()
        item['arrange']=response.xpath('//div[class = "th-bd2"]/span').extract()
        item['start_time'] =response.xpath('//div[class = "course-enroll-info_course-info_term-time"]/span').extract()[1]
        item['hours_arrange']=response.xpath('//div[class = "course-enroll-info_course-info_term-workload"]/span').extract()[1]
        item['full_description']=response.xpath('//div[class ="category-content"][0]/p/span').extract()
        item['aim'] = response.xpath('//div[class ="category-content"][1]/p').extract()
        item['outline'] = response.xpath('//div[class ="outline__new-outline"]').extract()
        item['need'] = response.xpath('//div[class ="category-content"][3]/p/span').extract()
        item['graduation'] = response.xpath('//div[class ="category-content"][4]/li').extract()
        item['reference'] = response.xpath('//div[class ="category-content"][5]/p').extract()
        yield item





















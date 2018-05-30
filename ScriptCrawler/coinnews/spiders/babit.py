# -*- coding: utf-8 -*-
import scrapy
from ..items import CoinnewsItem
from datetime import datetime

import dateutil
import dateutil.parser
import time

class BabitSpider(scrapy.Spider):
    name = 'babit'
    allowed_domains = ['8btc.com']
    start_urls = ['http://www.8btc.com/news']

    def parse(self, response):
        #找到所有快讯的块
        for article in response.xpath('//div[@id="list_content_all"]/article'):
            #找到快讯发布时间的块
            time_from_now = article.xpath('div[@class="article-content"]/div[@class="article-info clearfix"]/span/text()').extract_first()
            #判断是不是几分钟前
            if not time_from_now.endswith('分钟前'):
                break
            #获取快讯内容的链接
            url = article.xpath('div[@class="article-content"]/div[@class="article-title article-title_news"]/a/@href').extract_first()
            #传给下一级Parse获取详细的信息
            yield scrapy.Request(url=url, callback=self.parse_detail)                

    def parse_detail(self, response):
        #获取快讯的标题
        title = response.xpath('//div[@class="article-title"]/h1/text()').extract_first()
        detail = ""
        #快讯内容位置
        for p in response.xpath('//div[@class="article-content"]/p'):
            #获得具体快讯内容
            detail += p.xpath('./text()').extract_first()
        item = CoinnewsItem()
        item['content'] = '【' + title + '】' + detail
        #获取快讯发布时间
        strtime = response.xpath('//div[@class="single-crumbs clearfix"]/span/time/@datetime').extract_first()
        #替换时间，原因是格式不匹配
        date_str = strtime.replace('+08:00', '+0800')
        #转换格式datetime.strptime(date_string, format)：将格式字符串转换为datetime对象
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
　　　　　　　　#存放快讯发布时间,精确到毫秒
        item['time'] = int(dt.timestamp())*1000
        #快讯来源
        item['origin'] = '8bit'
        #爬取的快讯标记为false，意思是还没有传给目标数据库
        item['is_upload'] = False
        #快讯的id
        item['item_id'] = response.url.split('/')[-1]
　　　　　　　　#用于删除快讯的时间，自己加入时间作为索引
        #item['TTLtime'] = datetime.utcnow()

        #将快讯发布的时间作为索引，不自己添加时间
　　　　　　　 #获得快讯发布时间的时间戳
        timeStamp = int(dt.timestamp())
　　　　　　　　#将时间戳转为时间格式字符串
        timeArray = time.localtime(timeStamp)
        dateStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
　　　　　　　　#再将格式字符串转为mongodb识别的ISOdate的时间格式
        myDatetime = dateutil.parser.parse(dateStr)
　　　　　　　　#将ISOdate时间存入mongodb
        item['TTLtime'] = myDatetime
        yield item


            



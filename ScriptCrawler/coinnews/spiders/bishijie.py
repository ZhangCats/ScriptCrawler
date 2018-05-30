# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import CoinnewsItem
from datetime import datetime

import dateutil
import dateutil.parser
import time

class BishijieSpider(scrapy.Spider):
    name = 'bishijie'
    allowed_domains = ['bishijie.com']
    start_urls = ['http://www.bishijie.com/api/newsv17/index?size=100&client=pc']#请求地址(不需要签名)

    def parse(self, response):
        rjson = json.loads(response.text)
        for daily in rjson['data']:
            for news in daily['buttom']:
                item = CoinnewsItem()
                item['content'] = "【"+news['title']+"】"+news['content']
                item['item_id'] = news['newsflash_id']
                item['time'] = news['issue_time']*1000
                item['origin'] = "币世界"
                item['is_upload'] = False
                #item['TTLtime'] = datetime.utcnow()
                
                timeStamp = news['issue_time']
                timeArray = time.localtime(timeStamp)
                dateStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
                myDatetime = dateutil.parser.parse(dateStr)
                item['TTLtime'] = myDatetime
                yield item

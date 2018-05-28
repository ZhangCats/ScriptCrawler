# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
from ..items import CoinnewsItem

class JinseSpider(scrapy.Spider):
    name = 'jinse'
    allowed_domains = ['jinse.com']
    start_urls = ['https://api.jinse.com/v3/live/list?limit=100']#请求地址(不需要签名)

    def parse(self, response):
        rjson = json.loads(response.text)
        for daily in rjson['list']:#信息在list列表里
            for news in daily['lives']:#快讯在lives列表里
                item = CoinnewsItem()
                item['content'] = news['content']
                item['item_id'] = news['id']
                item['time'] = news['created_at']*1000
                item['origin'] = "金色财经"
                item['is_upload'] = False
                item['TTLtime'] = datetime.utcnow()
                yield item
        

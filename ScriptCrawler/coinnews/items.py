# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoinnewsItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()#快讯的内容
    origin = scrapy.Field()#快讯的来源（哪个网站）
    item_id = scrapy.Field()#快讯的id
    time = scrapy.Field()#快讯的发布时间
    is_upload = scrapy.Field()#全部初始化为False，意思是把爬取下来的快讯全都标记为未存入蜂巢的数据库，利用mongdb判断是否重复传入
    TTLtime = scrapy.Field()#用于删除快讯的时间

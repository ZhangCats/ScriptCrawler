# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

class CoinnewsPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'coinnews'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'coinnews_items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):#判断要写入的东西是否为空，不为空写入mongodb
        existed = self.db[self.collection_name].find_one({'item_id':item['item_id'], 'origin':item['origin']})
        if existed:
            raise DropItem('item has been collected.')
        else:
            self.db[self.collection_name].insert_one(dict(item))
            return item

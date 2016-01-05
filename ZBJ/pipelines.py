# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class ZbjPipeline(object):
#    def process_item(self, item, spider):
#        return item
import json
import codecs
from collections import OrderedDict

#import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
#from scrapy import log
import logging

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        log.msg("Tasks added to MongoDB database!", level=log.DEBUG, spider=spider) #log过时
        return item
            
            

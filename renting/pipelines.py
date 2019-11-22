# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class RentingPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['ziroom']

    def process_item(self, item, spider):
        self.db['rooms'].insert(dict(item))
        return item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import sys


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    """
    NOTE: This is not only use for development purpose. Do not use it in production.
    To enable MongoDBPipeline, be sure the it's uncommented in setting.py

    This is quick and dirty way for you to explore the data in mongodb
    which the data relation isn't important to you.
    """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        if not self.mongo_uri:
            sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_settings(cls, settings):
        return cls(
            mongo_uri=settings.get("MONGO_URI"),
            mongo_db=settings.get("MONGO_DB", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Start with a clean database
        self.db[spider.name].delete_many({})

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

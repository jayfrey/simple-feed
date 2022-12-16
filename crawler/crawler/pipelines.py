# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from crawler.utils.db_helper import escape_single_quote_value

import pymongo
import psycopg2
import sys


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    """
    NOTE: This is only use for development purpose. Do not use it in production.
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


class PostgresDBPipeline:
    """
    To enable PostgresDBPipeline, be sure the it's uncommented in setting.py
    """

    def __init__(self, postgres_details):
        self.postgres_details = postgres_details
        if not self.postgres_details:
            sys.exit("You need to provide a Connection Details.")

    @classmethod
    def from_settings(cls, settings):
        return cls(
            postgres_details=settings.get("POSTGRES_DETAILS"),
        )

    def open_spider(self, spider):
        self.client = psycopg2.connect(self.postgres_details)
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        """
        The following will perform insert if the item doesn't exist, otherwsie, it will
        update if there's a change in value. By default, it takes the spider name as table
        name, hence, be sure that your DB has a corresponding table name created
        """
        table = spider.table_name
        primary_fields = item.get_primary_fields()

        # Remove item that is either None, empty or hypen
        item.sanitise_items()

        # Escape single quote in value, this will return another copy of item because the use of the deepcopy()
        escaped_single_quote_items = escape_single_quote_value(item.deepcopy())

        fields = ",".join(item.keys())
        where_condition = " AND ".join(
            [f"{k}='{escaped_single_quote_items[k]}'" for k in primary_fields]
        )

        select_stmt = f"SELECT {fields} FROM {table} WHERE {where_condition}"

        self.cursor.execute(select_stmt)
        current_data = self.cursor.fetchone()

        if current_data:
            # Compare with the original items instance instead of the escaped_single_quote_items
            if current_data != tuple(item.values()):
                # Perform update if there's a change in value otherwise, skip update
                new_data = ",".join(
                    [f"{k}='{v}'" for k, v in escaped_single_quote_items.items()]
                )
                update_stmt = f"UPDATE {table} SET {new_data} WHERE {where_condition}"
                self.cursor.execute(update_stmt)
                self.client.commit()
        else:
            # Perform insert
            values = ",".join(
                ["'{0}'".format(v) for v in escaped_single_quote_items.values()]
            )
            insert_stmt = f"INSERT INTO {table} ({fields}) VALUES ({values})"
            self.cursor.execute(insert_stmt)
            self.client.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()

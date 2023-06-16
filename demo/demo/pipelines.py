# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import sys
from .items import VietstockItem

class MongoDBPipeline:

    collection = 'NewArticles'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # # Start with a clean database
        # self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(VietstockItem(item))
        # check if the item already exists
        # Define the criteria to check for existence
        criteria = {"url": item["url"]}

        # Execute the find operation with the defined criteria
        result = self.db[self.collection].find_one(criteria)

        # Check if the item exists
        if result:
            print("Item exists in the collection.")
        else:
            print("Item does not exist in the collection. Adding now.")
            self.db[self.collection].insert_one(data)
        return item
    

import pymongo
from pymongo.errors import DuplicateKeyError


class MongoPipeline:

    def open_spider(self, spider):
        self.my_cli = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.my_table = self.my_cli['spider_data'][f'{spider.name}']
        self.my_table.create_index([('url', 1)], unique=True)

    def close_spider(self, spider):
        self.my_cli.close()
        pass

    def process_item(self, item, spider):
        try:
            self.my_table.insert_one(dict(item))
        except DuplicateKeyError:
            pass

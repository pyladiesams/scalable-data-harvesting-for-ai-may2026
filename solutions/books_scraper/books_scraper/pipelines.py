# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pandas as pd
from itemadapter import ItemAdapter
from scrapy import Item


class BooksToCsv:
    def open_spider(self):
        self.rows = []

    def process_item(self, item: Item):
        self.rows.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self):
        df = pd.DataFrame(self.rows)
        df.to_csv("books.csv", index=False)

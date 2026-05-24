# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import datetime as dt
import json
import pathlib

import pandas as pd
from itemadapter import ItemAdapter
from scrapy import Item

from books_scraper.items import Book


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt.datetime):
            return o.isoformat()
        return super().default(o)


class BooksToCsv:
    def open_spider(self):
        self.rows = []

    def process_item(self, item: Item):
        self.rows.append(ItemAdapter(item).asdict())
        return item

    def close_spider(self):
        df = pd.DataFrame(self.rows)
        df.to_csv("books.csv", index=False)


class BooksToJsonFolder:
    FOLDER = pathlib.Path("./books").absolute()

    def open_spider(self):
        self.FOLDER.mkdir(exist_ok=True)

    def process_item(self, item: Book):
        with self.FOLDER.joinpath(item["upc"] + ".json").open(
            "w", encoding="utf-8"
        ) as f:
            json.dump(ItemAdapter(item).asdict(), f, cls=DateTimeEncoder)
        return item

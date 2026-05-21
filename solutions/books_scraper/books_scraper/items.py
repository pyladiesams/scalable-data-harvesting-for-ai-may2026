# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime as dt

import scrapy


class Book(scrapy.Item):
    url: str = scrapy.Field()
    scraped_at: dt.datetime = scrapy.Field()

    upc = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    availability = scrapy.Field()

import datetime as dt

import scrapy
from scrapy.http import Response

from books_scraper.items import Book


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response):
        """Extract book links and pagination."""
        page_links = response.css("h3 a::attr(href)")
        next_page = response.css(".next").css("a::attr(href)").get()

        for link in page_links:
            yield response.follow(
                url=link,
                callback=self.parse_books,
            )
        yield response.follow(next_page, callback=self.parse)

    def parse_books(self, response: Response):
        book = Book()

        book["url"] = response.url
        book["scraped_at"] = dt.datetime.now(dt.timezone.utc)

        book["title"] = response.css("h1::text").get()
        book["price"] = response.css(".price_color::text").get()
        book["description"] = (
            response.css("div#product_description")
            .xpath("following-sibling::p[1]/text()")
            .get()
        )
        book["rating"] = response.css(".star-rating::attr(class)").get()

        table = {}
        for row in response.css("table tr"):
            key = row.css("th::text").get()
            item = row.css("td::text").get()
            table[key] = item

        book["upc"] = table.get("UPC")
        book["availability"] = table.get("Availability")

        return book

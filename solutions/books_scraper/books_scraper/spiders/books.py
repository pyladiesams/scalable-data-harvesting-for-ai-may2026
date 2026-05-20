import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    ]

    def parse(self, response):
        pass

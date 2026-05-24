import redis
import scrapy
from scrapy.http import Response

from books_scraper.settings import QUEUE_KEY, REDIS_URL


class PaginationSpiderSpider(scrapy.Spider):
    name = "pagination_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.redis = redis.Redis.from_url(REDIS_URL)
        self.queue_key = QUEUE_KEY

    def parse(self, response: Response):
        page_links = response.css("h3 a::attr(href)")

        # Worker spiders will make requests outside of the context
        # of this specific request so URLs need to be absolute!
        product_urls = [response.urljoin(href) for href in page_links.getall()]

        self.redis.lpush(self.queue_key, *product_urls)

        next_page = response.css(".next").css("a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

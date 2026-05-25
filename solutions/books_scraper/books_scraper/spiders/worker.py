import datetime as dt

from scrapy.http import Response
from scrapy_redis.spiders import RedisSpider

from books_scraper.items import Book
from books_scraper.settings import QUEUE_KEY


class WorkerSpider(RedisSpider):
    name = "worker"
    redis_key = QUEUE_KEY

    max_idle_time = 2

    def parse(self, response: Response):
        book = Book()

        # URL and datetime are just metadata
        book["url"] = response.url
        book["scraped_at"] = dt.datetime.now(dt.timezone.utc)

        # The title is the text inside the only h1 element on this page
        book["title"] = response.css("h1::text").get()

        # The price is the text of an element with a specific css class.
        book["price"] = response.css(".price_color::text").get()

        # The description can be a bit more tricky.
        # Option 1: Take all elements with HTML tag p and use the text of the last one
        # response.css("p::text").get()

        # Option 2: Find the element with ID 'product_description', use an
        # xpath selector to get the next sibling, and then extract the text from
        # that sibling.
        book["description"] = (
            response.css("div#product_description")
            .xpath("following-sibling::p")
            .css("p::text")
            .get()
        )

        # For the rating, we can extract the whole CSS class name, which will be
        # something like 'star-rating three', we can parse this later into an
        # integer, but in the spider we should focus on extraction alone.
        book["rating"] = response.css(".star-rating::attr(class)").get()

        # For UPC and Availability we can use the position of the information
        # within the product information table
        book["upc"] = response.css("td::text")[0].get()
        book["availability"] = response.css("td::text")[-2].get()

        yield book

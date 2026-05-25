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
        # We extract all the hyperlinks from anchors within h3 headings.
        # Using the browser or scrapy's webview, we can identify them as
        # the elements containing the product links.
        page_links = response.css("h3").css("a::attr(href)")

        # Conveniently, there exists a 'next' CSS class from which we can
        # retrieve the anchor and the associated link to the next page
        next_page = response.css(".next").css("a::attr(href)").get()

        for link in page_links:
            # For each link in the link queue we 'follow' the href in the
            # context of the current response. The response for this request is
            # then passed again to self.parse.
            # Note, that relative hrefs are OK here, because scrapy will
            # resolve them using the current response as the context in the same
            # way as a browser would.
            yield response.follow(
                url=link,
                callback=self.parse_books,
            )

        # Continue if we are not at the end
        # If no additional page was found, there is nothing to do anymore
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_books(self, response: Response):
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

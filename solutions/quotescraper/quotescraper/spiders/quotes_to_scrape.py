from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        # Two static pages and one JS-rendered page. Scraping all three lets
        # us compare what Scrapy receives when JavaScript is and isn't involved.
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
            "https://quotes.toscrape.com/js/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Save each page's raw HTML to a file named after its page number.
        # Open the files afterwards: the static pages contain the quotes,
        # but the /js/ page does not, because Scrapy never ran its JavaScript.
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
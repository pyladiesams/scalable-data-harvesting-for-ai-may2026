from pathlib import Path
import scrapy

class JSQuotesSpider(scrapy.Spider):
    name = "js_quotes"
    
    async def start(self):
        url = "https://quotes.toscrape.com/js/"
        
        yield scrapy.Request(url=url, callback=self.parse, meta={"playwright": True})
        # Makes scrapy route the request specifically through playwright.
        
        
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall()
            }
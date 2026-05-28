import scrapy


class JSQuotesSpider(scrapy.Spider):
    name = "js_quotes"

    async def start(self):
        # The /js/ version of the site renders its quotes with JavaScript,
        # so a plain request would return a page with no quotes in the HTML.
        url = "https://quotes.toscrape.com/js/"

        # The playwright meta flag routes this request through a headless
        # browser, which runs the JavaScript before handing the page back.
        yield scrapy.Request(url=url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        # By now Playwright has rendered the page, so the quote elements
        # exist in the HTML and our selectors can find them.
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
# Scalable Data Harvesting for AI - Workshop

In this workshop we will go over some techniques to scrape large amounts of data from websites.
Specifically we, will be looking at [scrapy](https://www.scrapy.org/), one of the world's most popular open source data extraction frameworks, specifically engineered to collect the amounts of data necesseary for modern AI models.

The below exercises will walk you through the workshop and to your first own spiders.
For the educational purposes of this workshop we will focus on [books.toscrape.com](https://books.toscrape.com/).
This is a site that is specifically intended to be craped. Please be aware that other sites might ban you if you send too many requests in a too small amount of time!

If you are stuck, or need inspiration, check out the [solutions](../solutions/README.md)!

## Exercise 0 - Creating a new Scrapy Project and Spider

Scrapy projects contain the configurations, pipelines and extraction rules for your scrapers. 

1. Create a new Project
```bash
cd workshop/ # If you are not already in the workshop directory
scrapy startproject PROJECT_NAME PROJECT_DIR
```
Where `PROJECT_NAME` is an arbitrary name that you would like to give your scraping project and `PROJECT_DIR` optionally specifies the directory for your project. `cd` into yoru new project directory and take note of all the files that scrapy created for you. We will be working with these files later in the workshop.

2. Creating a new spider
After usign `cd` to enter your project folder use the scrapy CLI again to create a new, empty spider:
```bash
scrapy genspider NAME DOMAIN
```
Where `NAME` is the name of the spider by which it will be referenced inside your project and `DOMAIN` is the domain your spider is intended to scrape. This is used so that the spider does not follow links to unintended places.

3. Confirm that your spider is set up and can connect to the target page.
```bash
scrapy crawl NAME
```
You should see a bunch of scrapy specific stats and crucially:
```bash
2026-05-25 10:29:22 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://books.toscrape.com> (referer: None)
```

## Exercise 1 - Selectors and Data Extraction

In this exercise we will learn how to extract data from a webpage and write it to an output location.

1. Select any book from [books.toscrape.com](https://books.toscrape.com/index.html)
2. Paste the URL of your book into the `start_urls` attribute of the spider your have created in exercise 0. For the purpose of this exercise, your chosen URL should be the only element in that list.
3. To confirm, run your spider one more time with `scrapy crawl NAME`. You should see e.g.:
```bash
2026-05-25 10:46:30 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html> (referer: None)
```
4. Examine your chosen book and decide what you would like to scrape. E.g. title, price, availability, etc...
- Define the your scraping schema in the `items.py` file of your project. This step is somewhat optional, but working with a predefined schema is considered best practice in large scale scraping projects. Scrapy even gets you started with a template class! Tip: Metadata like the URL and the scraping time can and arguably should be part of your `Item`. Donstream processes can convert `Items` to dictionaries e.g. by using `itemadapter.ItemAdapter(item).asdict()`.
5. Populate the `parse` method of your spider with the appropriate selectors. Example:
```python
def parse(self, response: Response):
    book = items.Book()

    # The title is the only h1 element on the page and we would like to extract
    # the text from this element. We fall back to a generic label if no title is
    # found.
    book["title"] = response.css('h1::text').get("<title not found>")
    # There is only one img element on the page and we would like to extract its
    # src attribute
    book["image_link"] = response.css("img::attr(src)").get('<image not found>')

    ...

    yield book
```
You can find a reference for selector rules in this [Cheat Sheet](../docs/selector_reference.md).
You can use the scrapy interactive shell to experiment with different extractors. Open the shell via `scrapy shell URL`. The shell provides a `response` object which you can extract from (with `response.css(...)`) or you can display the page in your default as 'scrapy sees it' with `view(response)`.

> It is commonly considered best practice to focus purely on extraction at this step. You might be tempted to start cleaning data, but thsi would typically happen in the ItemPipeline.

6. Bonus: If you are extra fast and ambitious, you can also set up an item pipeline for cleanign and to write custom output. This step is somewhat optional at this stage, but will be required for distributed scraping later on.
- Find the `pipelines.py` module of your project. Scrapy already gets you started with a dummy class! You can use the `process_item` method to clean items and write them to a file or Database.
> Tip: If you need to take some action at the beginning of the scraping process (e.g. connecting to a Database) or at the end of the project (e.g. flushing a buffer to disk or closing a connection), you can use the `open_spider` or `close_spider` methods.
- After you have defined your ItemPipeline, don't forget to add it to your spider by finding and uncommenting the `ITEM_PIPELINES` variable in the `settings.py` file of your project.
> Tip: It is commonly considered good practice to split cleaning and persisting items into separate pipelines. You can add multiple item pipelines to `ITEM_PIPELINES` and denote their priority with the dictionary value. Lower values run first!

7. Run your spider again with `scrapy crawl NAME -O output.csv`. The `-O` option denotes the output file. If you have defined your own item pipeline, you can skip this option. If your spider finishes you should see your output file in your project with exactly one row of content!

## Exercise 2 - Pagination and Following Links

In exercise 2 we will learn about following links and pagination. This is crucial to find and scrape the pages that you are actually interested in.
1. Find the `start_url` attribute of your spider and paste the landing page URL of `books.toscrape.com` into it. For the purpose of this exercise, that should be the only element in the list.
2. Use the scrapy interactive shell, to find a way of extracting the links to the individual products and also to the next page.
> Tip: Some pages (books.toscrape.com included) make it easy to _derive_ the page links, so that you do not actually have to scrape them. You might have to only scrape the page number of the last page and can use that to construct a list of URLs to scrape.
3. In the `parse` method of your spider, extract the links and follow them with `response.follow(url=..., callback=...)`. At this stage you should probably move the item parsing logic out of your `parse` method. Example:
```python
def parse(self, response: Response):
    book_links = response.css(...)
    next_page = response.css(...)

    for link in book_links:
        yield response.follow(url=link, callback=self.parse_book)
    
    # Using a guard, since you will likely not find a link on the last page.
    if next_page:
        yield response.follow(...)

def parse_book(self, response: Respone):
    """Should contain the logic that you derived in the previous exercise."""
    ...
```
4. Run your spider again with `scrapy crawl NAME -L INFO -O output.csv`. If the spider runs successful, you should have a CSV with 1,000 rows of content.
> Tip: The `-L` option helps us to control the log level, which defaults to `DEBUG` setting it to `INFO` is optional but prevents the terminal being flooded outside of a debugging context.

5. Bonus: Depending on network speed and hardware capacity, you will probably observe scraping speeds of 30 - 60 items per minute. That is much too slow if you aim to scrape millions of pages! To speed things up, you can find the `DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS` and `CONCURRENT_REQUESTS_PER_DOMAIN` settings in the `settings.py` file of your project. Try setting the concurrent requests (per domain) to 64 and the download delay (in seconds) to 0 and observe the speed increase on your next run!
>Tip: The `DOWNLOAD_DELAY` settings is very useful if you want to adhere to specific API rate limit, but for typical webscraping autothrottling is usually sufficient and more useful.

## Exercise 3a - Parsing JS and working with a Headless Browser
TODO

## Exercise 3b - Distributed Scraping
Distributed scraping is where scrapy really shines. Properly set up, the only limits to your scraping is how much hardware you can afford!

1. Distributed scraping with scrapy requires the package `scrapy-redis`, as redis is used as the queue for URLs to scrape. Add it to your environment with `uv add scrapy-redis`.
2. You will need a running Redis instance. For that, you can use the redis service in the provided [docker-compose.yml](../solutions/docker-compose.yml) file. Start it with e.g. `docker compose up --service redis`. The default URL will be `http://localhost:6379`. Add this URL to your project's `settings.py` as `REDIS_URL`.
3. Decide on a `QUEUE_KEY` for URLs to scrape. Any URLs that are added to this queue in Redis will be popped by your worker spider and scraped. Add the `QUEUE_KEY` to your `settings.py` as well.
4. Create a new spider. Modify the new spider to inherit from `scrapy_redis.RedisSpider` (instead of the default `scrapy.Spider`) and replace the `allowed_domans` and `start_urls` attribute with `redis_key` (which should be equal to your `QUEUE_KEY`) and `max_idle_time`. The latter controls how long the RedisSpider will stay idle after the queue is empty before it shuts down in seconds. Populate the `parse` method of this new spider with the book parsing logic derived in exercise 1. You now have a spider that can scrape from a queue.
5. Now you need a way to populate the queue. Create another regular spider, and put the link derivation logic you derived in exercise 2 in the parse method of this new spider. The main difference: This time you enqueue the links to books to on your redis instance, so that other spiders take over the scraping of actual elements. Example:
```python
class PaginationSpider(scrapy.Spider):
    ...

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        # Connect to your redis instance
        self.redis = redis.Redis.from_url(settings.REDIS_URL)
        self.queue_key = settings.QUEUE_KEY

def parse(self, response: Response):
    book_links = response.css(...)
    next_page = response.css(...)

    # Since the worker spiders will make the requests outside of the context of this response, they will require the absolute URLs!
    book_pages_absolute = [
        response.urljoin(href) for href in book_links.getall()
        ]
    self.redis.lpush(self.queue_key, *book_pages_absolute)

    ... # Follow the next page as before.
```
6. Before running your distributed scraping job, you need some way of preventing multiple worker psiders overriding each other's output. The simplest option is to run the separate worker spider's with dedicated output file names, e.g. `scrapy crawl worker -O worker_1.csv & scrapy crawl worker -O worker_2.csv & ...`. The more advanced method is create a pipeline that writes incrementally to a shared output location, e.g. JSON files stored in a folder, as demonstrated [here](../solutions/books_scraper/books_scraper/pipelines.py#L40).
7. For distributed scrapin, scrapy's internal scheduler and duplication filter need to run on redis as well, instead of in-memory. To do so, add these lines to your `settings.py`:
```python
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
```
8. When running your spider, make sure that redis is up. Then you can run your distributed scraping process with:
```bash
scrapy crawl pagination_spider -L INFO &
    scrapy crawl worker -L INFO &
    scrapy crawl worker -L INFO &
    scrapy crawl worker -L INFO # Repeat ad-nauseum (or crash :))
```
An arguably more elegant of deploying multiple spiders is shown in the [docker-compose](../solutions/docker-compose.yml) file in the solutions.

# Scalable Data Harvesting for AI - Workshop

In this workshop we will go over some techniques to scrape large amounts of data from websites.
Specifically we, will be looking at [scrapy](https://www.scrapy.org/), one of the world's most popular open source data extraction frameworks, specifically engineered to collect the amounts of data necesseary for modern AI models.

The below exercises will walk you through the workshop and to your first own spiders.
For the educational purposes of this workshop we will focus on [books.toscrape.com](https://books.toscrape.com/).
This is a site that is specifically intended to be craped. Please be aware that other sites might ban you if you send too many requests in a too small amount of time!

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

> It is commonly considered best practice to focus purely on extraction at this step. You might be tempted to start cleaning data, but thsi would typically happen in the ItemPipeline.

6. Bonus: If you are extra fast and ambitious, you can also set up an item pipeline for cleanign and to write custom output. This step is somewhat optional at this stage, but will be required for distributed scraping later on.
- Find the `pipelines.py` module of your project. Scrapy already gets you started with a dummy class! You can use the `process_item` method to clean items and write them to a file or Database.
> Tip: If you need to take some action at the beginning of the scraping process (e.g. connecting to a Database) or at the end of the project (e.g. flushing a buffer to disk or closing a connection), you can use the `open_spider` or `close_spider` methods.
- After you have defined your ItemPipeline, don't forget to add it to your spider by finding and uncommenting the `ITEM_PIPELINES` variable in the `settings.py` file of your project.
> Tip: It is commonly considered good practice to split cleaning and persisting items into separate pipelines. You can add multiple item pipelines to `ITEM_PIPELINES` and denote their priority with the dictionary value. Lower values run first!

7. Run your spider again with `scrapy crawl NAME -O output.csv`. The `-O` option denotes the output file. If you have defined your own item pipeline, you can skip this option. If your spider finishes you should see your output file in your project!

## Exercise 2 - Pagination and Following Links

## Exercise 3a - Parsing JS and working with a Headless Browser

## Exercise 3b - Distributed Scraping
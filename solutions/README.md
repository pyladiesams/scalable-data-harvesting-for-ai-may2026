# Scalable Data Harvesting for AI - Solutions

Use the content of this folder if you get stuck during the exercises or are looking for inspiration and examples.

## Contents
### books.py
[This](./books_scraper/books_scraper/spiders/books.py) file contains the full basic spider for scraping and the solution for exercises 1 and 2.
Note that it uses the [Book](./books_scraper/books_scraper/items.py) item and the [BooksToCsv](./books_scraper/books_scraper/pipelines.py#L27) pipeline.
When in the project directory it can be run with `scrapy crawl books`, but not t

### pagination_spider.py
[This](./books_scraper/books_scraper/spiders/pagination_spider.py) file contains the pagination spider that is used to populate the redis queue for exercise 3.

### worker.py
[This](./books_scraper/books_scraper/spiders/worker.py) contains the worker spider that dequeues the URLs that have previously been enqueued by the pagination spider and scrapes the individual books.

### docker-compose.yml
[This](./docker-compose.yml) file contains and example stack that runs the distributed scraping process with an adjustable number of worker replicas.

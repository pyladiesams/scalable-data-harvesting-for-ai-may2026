import os

from books_scraper.books_scraper.spiders.books import BooksSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

os.environ["SCRAPY_SETTINGS_MODULE"] = "books_scraper.settings"


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    process.crawl(BooksSpider)
    process.start()


if __name__ == "__main__":
    main()

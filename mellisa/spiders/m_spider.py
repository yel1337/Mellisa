import scrapy
import os
from misc.misc_prompts import Misc
from scrapy.loader import ItemLoader
from items import MellisaItem
from pathlib import Path

class ScrapeParameters(scrapy.Spider):
    name = "param_spider"
    start_urls = []

    def __init__(self, url=None, start_urls=None, *args, **kwargs):
        super(ScrapeParameters, self).__init__(*args, **kwargs)
        self.datas = []
        self.data_len = 0

        if url:
            self.start_urls = [f"{url}"]
        elif start_urls:
            self.start_urls = start_urls
    # ignore comments ("#") and empty lines ("//") in wordlist.txt
    def load_xpath(self, file_path):
        try:
            with open(file_path, "r") as f:
                return [line.strip()
                        for line in f
                        if line.strip() and not line.lstrip().startswith("#") and not line.lstrip().startswith("//")
                ]
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return []

    # Return Num Callback
    def return_num_data(self, data_len):
        if data_len > 0:
            return True

    # Return None Callback
    def return_none(self, data_len):
        if data_len == 0:
            return True

    def _add_val_item(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("item_param", datas)

        return loader.load_item()

    def _add_val_url(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("urls", datas)
        return loader.load_item()

    def crawl_page(self, query, response):
        next_pages = response.xpath(query)
        urls = next_pages.getall()

        for url in urls:
            if url:
                yield response.follow(url, callback=self.parse)

    def parse(self, response):
        try:
            # assumes wordlist.txt is in the same dir as m_spiders.py's parent (i.e. /mellisa/)
            path = Path(__file__).resolve().parent.parent / "wordlist.txt"
            query = Path(__file__).resolve().parent.parent / "page_queries.txt"

            xpaths = self.load_xpath(path)
            query_xpath = self.load_xpath(query)

            # Safe handling of xpath lists
            if isinstance(xpaths, list) and xpaths:
                xpaths = xpaths[0]
            else:
                xpaths = ""
                self.logger.warning("No valid XPath patterns found in wordlist.txt")

            if isinstance(query_xpath, list) and query_xpath:
                query_xpath = query_xpath[0]
            else:
                query_xpath = ""

            # Extract data with error handling
            if xpaths:
                extracted_datas = response.xpath(xpaths).getall()
                self.datas.extend(extracted_datas)

                load_item = self._add_val_item(extracted_datas, response)
                yield load_item

            # Crawl linked pages if query exists
            if query_xpath:
                for page in self.crawl_page(query_xpath, response):
                    yield page

        except Exception as e:
            self.logger.error(f"Error parsing response from {response.url}: {e}")

    def closed(self, reason):
        misc = Misc()
        data_len = len(self.datas)
        if self.datas:
            misc.misc_saving(self.datas, self.return_num_data(data_len))
            self.return_num_data(data_len)
            misc.misc_output()
        elif data_len == 0:
            misc.misc_none()

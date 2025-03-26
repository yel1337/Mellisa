import scrapy
import os
from scrapy.loader import ItemLoader
from misc.misc_prompts import Misc
from items import MellisaItem


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

    def load_xpath(self, file_path):
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]

    # Return Num Callback
    def return_num_data(self, data_len):
        if data_len > 0:
            return True

    # Return None Callback
    def return_none(self, data_len):
        if data_len == 0:
            return True

    # Add arg to item.py
    def _add_val_item(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("item_param", datas)

        return loader.load_item()

    # Add url arg to item.py
    # A function which stores extracted href links to item.py
    def _add_val_url(self, url, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("urls", url)

    def crawl_page(self, query, response):
        next_pages = response.xpath(query)
        urls = next_pages.getall()

        for url in urls:
            if url:
                yield response.follow(url, callback=self.parse)

    def parse(self, response):
        # xpath queries for crawling page CONTENTS
        path = os.path.join(
            os.path.expanduser("~"),
            "Mellisa_src/mellisa/wordlist.txt"
        )
        # xpath queries for crawling href which redirects to PAGES
        query = os.path.join(
            os.path.expanduser("~"),
            "Mellisa_src/mellisa/page_queries.txt"
        )

        xpaths = self.load_xpath(path)
        query_xpath = self.load_xpath(query)

        if isinstance(xpaths, list):
            xpaths = xpaths[0] if xpaths else ""

        if isinstance(query_xpath, list):
            query_xpath = query_xpath[0] if query_xpath else ""

        extracted_datas = response.xpath(xpaths).extract()
        self.datas.extend(extracted_datas)

        load_item = self._add_val_item(extracted_datas, response)
        yield load_item

        crawl_page = self.crawl_page(query_xpath, response)
        load_url = self._add_val_url(crawl_page, response)

        yield load_url

    def closed(self, reason):
        misc = Misc()
        data_len = len(self.datas)
        if self.datas:
            misc.misc_saving(self.datas, self.return_num_data(data_len))
            self.return_num_data(data_len)
            misc.misc_output()
        elif data_len == 0:
            misc.misc_none()

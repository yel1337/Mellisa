import scrapy
import os
from scrapy.loader import ItemLoader
from mellisa_base.items import MellisaItem
from pathlib import Path

class ScrapeParameters(scrapy.Spider):
    name = "param_spider"
    start_urls = []

    def __init__(self, url=None, data_len=0, datas=None, start_urls=None, *args, **kwargs):
        super(ScrapeParameters, self).__init__(*args, **kwargs)
        self.datas = datas if datas is not None else []
        self.data_len = data_len if data_len > 0 else self.return_num_data()
        self.custom_xpath = kwargs.get('custom_xpath')

        # Running flag return True if custom xpath query is provided
        # otherwise return False
        self.running_custom = bool(self.custom_xpath)

        if url:
            self.start_urls = [f"{url}"]
        if start_urls:
            self.start_urls = start_urls

    # ignore comments ("#") and empty lines ("//") in wordlist.txt
    def load_xpath(self, file_path):
        with open(file_path, "r") as f:
            return [line.strip()
                    for line in f
                    if line.strip() and not line.lstrip().startswith("#") and not line.lstrip().startswith("//")
            ]

    # Return Num Callback
    def return_num_data(self):
        if self.datas:
            return len(self.datas)

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

    def crawl_page(self, query, response):
        next_pages = response.xpath(query)
        urls = next_pages.getall()

        for url in urls:
            if url:
                yield response.follow(url, callback=self.parse)

    def parse(self, response):
        # assumes wordlist.txt is in the same dir as m_spiders.py's parent (i.e. /mellicd sa/)
        path = Path(__file__).resolve().parent.parent / "wordlist.txt"
        query = Path(__file__).resolve().parent.parent / "page_queries.txt"

        if self.running_custom:
            print("Spider: Running using Custom...")
            extracted_datas_CUSTOM = response.xpath(self.custom_xpath).getall()

        xpaths = self.load_xpath(path)
        query_xpath = self.load_xpath(query)

        if isinstance(xpaths, list):
            xpaths = xpaths[0] if xpaths else ""
        
        if isinstance(query_xpath, list):
            query_xpath = query_xpath[0] if query_xpath else ""

        if xpaths:
            print("Spider: Running in default mode")
            extracted_datas = response.xpath(xpaths).getall()
            
        self.datas.extend(extracted_datas)

        load_item = self._add_val_item(extracted_datas, response)
        yield load_item

        crawl_page = self.crawl_page(query_xpath, response)
        load_url = self._add_val_url(crawl_page, response)

        yield load_url

    def closed(self, reason):
        from mellisa_base.misc.misc_prompts import Misc
        misc = Misc()
        if self.datas:
            misc.misc_saving(self.datas, self.data_len, self.return_num_data())
            misc.misc_output()
        elif self.data_len == 0:
            misc.misc_none()

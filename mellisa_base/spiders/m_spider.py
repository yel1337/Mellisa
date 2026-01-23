import scrapy
import os
from scrapy.loader import ItemLoader
from items import MellisaItem
from pathlib import Path

class ScrapeParameters(scrapy.Spider):
    name = "param_spider"
    start_urls = []

    def __init__(self, url=None, data_len=0, datas=None, start_urls=None, *args, **kwargs):
        super(ScrapeParameters, self).__init__(*args, **kwargs)
        self.datas = []
        self.data_len = 0
        self.custom_xpath = kwargs.get('custom_xpath')
        self.value_from_main = None
        self.args_url = url

        # running flag return True if custom xpath query is provided
        # otherwise return False
        self.running_custom_flag = bool(self.custom_xpath)
        self.running_default = None

        if url:
            self.start_urls = [f"{url}"]
        if start_urls:
            self.start_urls = start_urls

    # ignore comments ("#") and empty lines ("//") in wordlist.txt
    #
    # USE FOR DEFAULT 
    def load_xpath_default(self, file_path):
        try:
            with open(file_path, "r") as f:
                return [
                    line.strip()
                    for line in f
                    if line.strip()
                    and not line.lstrip().startswith("#")
                    and not line.lstrip().startswith("//")
                ]
        except FileNotFoundError:
            self.logger.error(f"File not found: {Path(file_path).name}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading {Path(file_path).name}: {type(e).__name__}")
            return []

    # USE FOR CUSTOM 
    def load_xpath_custom(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    # return Num Callback
    def return_len_data(self):
        if self.datas:
            return len(self.datas)

    # return None Callback
    def return_none(self, data_len):
        if data_len == 0:
            return True

    # return if has data
    def return_has_data(self, data):
        if data:
            return True
        else:
            return False

    def _add_value_item(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("item_param", datas)

        return loader.load_item()

    def _add_value_url(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("urls", datas)

    def crawl_page(self, query, response):
        next_pages = response.xpath(query)
        urls = next_pages.getall()

        for url in urls:
            if url:
                yield response.follow(url, callback=self.parse)

    def parse(self, response=None):
        # assumes wordlist.txt is in the same dir as m_spiders.py's parent
        path = Path(__file__).resolve().parent.parent / "wordlist.txt"
        query = Path(__file__).resolve().parent.parent / "page_queries.txt"
        
        # if default args then this will be use
        # otherwise if custom args is true 
        # query_xpath variable will be use instead
        xpaths = self.load_xpath_default(path)
        query_xpath = self.load_xpath_custom(query)

        if isinstance(xpaths, list):
            xpaths = xpaths[0] if xpaths else ""    
        elif isinstance(query_xpath, list):
            query_xpath = query_xpath[0] if query_xpath else ""
        
        if self.running_custom_flag is True:
            self.value_from_main = True
            extracted_datas_CUSTOM = response.xpath(self.custom_xpath).getall()
            self_datas = extracted_datas_CUSTOM
            self.datas.extend(extracted_datas_CUSTOM)

            load_item = self._add_value_item(extracted_datas_CUSTOM, response)
            yield load_item
        else:
            extracted_datas = response.xpath(xpaths).getall()
            self_datas = extracted_datas
            self.datas.extend(extracted_datas)

            load_item = self._add_value_item(extracted_datas, response)
            yield load_item

        from misc.misc_prompts import Misc    
        from mellisa import main
        data_len = self.return_len_data()
        datas = self.return_has_data(self.datas)
        misc = Misc(data_len, datas, self.value_from_main, self.args_url)

        if datas is True:
            return misc.misc_saving(datas, data_len, self.value_from_main)
        else:
            none = misc.misc_none()
            print(f"{none}")

        # crawl beneath the page and look for hyperlinks to crawl to
        crawl_page = self.crawl_page(query_xpath, response)
        load_url = self._add_value_url(crawl_page, response)

        yield load_url

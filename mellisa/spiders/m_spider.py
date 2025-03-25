import scrapy
import os
from misc.misc_prompts import Misc
from scrapy.loader import ItemLoader
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

    def _add_val_(self, datas, response):
        loader = ItemLoader(item=MellisaItem(), response=response)
        loader.add_value("item_param", datas)

        return loader.load_item()

    def parse(self, response):
        path = os.path.join(os.path.expanduser(
            "~"), "Mellisa_src/mellisa/wordlist.txt")

        xpaths = self.load_xpath(path)

        if isinstance(xpaths, list):
            xpaths = xpaths[0] if xpaths else ""

        extracted_datas = response.xpath(xpaths).extract()
        self.datas.extend(extracted_datas)

        load_item = self._add_val_(extracted_datas, response)
        yield load_item

        if load_item:
            next_page = response.xpath("//li/a/@href").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        misc = Misc()
        data_len = len(self.datas)
        if self.datas:
            misc.misc_saving(self.datas, self.return_num_data(data_len))
            self.return_num_data(data_len)
            misc.misc_output()
        elif data_len == 0:
            misc.misc_none()

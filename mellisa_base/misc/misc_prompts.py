import time
from mellisa import main, run_spider
from datetime import datetime
from typing import Optional
from spiders.m_spider import ScrapeParameters
from custom.log.log_custom import log_level, log
from misc.messages import Messages
from pathlib import Path


class Misc:
    def __init__(self, len_of_data, data, value_main):
        self.output_log = log
        self.msg = Messages()
        self.data_len = len_of_data
        self.data = data
        self.value_main = value_main

    def time_of_execution(self, message, datas=None, return_none_callback=None, return_data_callback=None):
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger = log_level(datas, message, return_none_callback,
                        return_data_callback)

        formatted_message = f"{execution_time} {logger} {message}"
        return formatted_message

    def misc_start(self):
        start_result = self.time_of_execution(f"{self.msg.for_info[0]}")
        time.sleep(2)
        return start_result

    def misc_none(self):
        none_result = self.time_of_execution(f"{self.msg.for_warning[0]}")
        return none_result

    def misc_has_len(self, data_len):
        return f"{self.msg.for_info[3]} {data_len}"

    def misc_on_default(self):
        return f"{self.msg.for_info[4]}"

    def misc_output(self):
        print("")
        output_filePath = Path(__file__).resolve().parent.parent / "output"  
        print(f"Output file saved in: {output_filePath}/domain_name.json")

    def misc_saving(self, data_len, main_val, return_none_callback=None, return_data_callback=None):
        crawling = self.time_of_execution(self.msg.for_info[0], self.data, return_data_callback)
        print(f"{crawling}")

        if self.value_main is None:
            default = self.time_of_execution(self.msg.for_info[4])
            print(f"{default}")
        elif self.value_main is True:
            custom = self.time_of_execution(self.msg.for_info[5])
            print(f"{custom}")

        if self.data:
            print(self.time_of_execution(
                self.msg.for_info[1], self.data, return_none_callback, return_data_callback))
        if run_spider:
            print(self.time_of_execution(
                self.msg.for_info[2], self.data, return_none_callback, return_data_callback))
        time.sleep(2)
        if self.data_len:
            print(f"{self.time_of_execution(self.msg.for_info[6])}: {self.data_len}")
            time.sleep(1)
        elif not self.data:
            raise Exception("No scraped data from pipeline")

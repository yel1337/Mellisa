import time
from datetime import datetime
from custom.log.log_custom import log_level

class Misc:
    def time_of_execution(self, message, datas=None, return_none_callback=None, return_data_callback=None):
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if return_data_callback is None:
            return_data_callback = lambda: bool(datas)
        if return_none_callback is None:
            return_none_callback = lambda: not bool(datas)

        log = log_level(datas, message, return_none_callback, return_data_callback)

        if message in ["Scraping...", 
                       "Saving...", 
                       "PARAMETERS FOUND",
                       "Page might not contain any parameter/s to be extracted, maybe try another one?"]:
            return f"{execution_time} {log} {message}"

    def misc_start(self, start_spider):
        if start_spider:
            print(self.time_of_execution("Crawling..."))
            time.sleep(2)
    
    def misc_none(self):
        message = "Page might not contain any parameter/s to be extracted, maybe try another one?"
        print(self.time_of_execution(message))

    def misc_has_len(self, data_len):
        message = f"Total number of scraped parameter/s from page: {data_len}"
        return message
    
    def misc_output(self):
        print("")
        output_filePath = "/home/user/Mellisa/mellisa/mellisa/output/domain.json"
        print(f"Output file saved in: {output_filePath}")

    def misc_saving(self, datas, return_none_callback=None, return_data_callback=None):
        if datas:
            print(self.time_of_execution("PARAMETERS FOUND", datas, return_data_callback))
            print(self.time_of_execution("Scraping...", datas, return_none_callback, return_data_callback))
            print(self.time_of_execution("Saving...", datas, return_none_callback, return_data_callback))
            time.sleep(2)
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO] Total number of scraped parameter/s from page: {len(datas)}")
            time.sleep(1)

    
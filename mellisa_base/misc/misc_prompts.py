import time
from datetime import datetime
from mellisa_base.custom.log.log_custom import log_level
from mellisa_base.misc.messages import Messages
from pathlib import Path
from mellisa_base.spiders.m_spider import ScrapeParameters

msg = Messages()


class Misc:
    def time_of_execution(self, message, datas=None, return_none_callback=None, return_data_callback=None):
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if return_data_callback is None:
            def return_data_callback(): return bool(datas)
        if return_none_callback is None:
            def return_none_callback(): return not bool(datas)

        log = log_level(datas, message, return_none_callback,
                        return_data_callback)

        if message in msg.for_info:
            return f"{execution_time} {log} {message}"
        elif message in msg.for_warning:
            return f"{execution_time} {log} {message}"

    def misc_start(self):
        print(self.time_of_execution(msg.for_info[0]))
        time.sleep(2)

    def misc_none(self):
        print(self.time_of_execution(msg.for_warning[0]))

    def misc_has_len(self, data_len):
        return f"{msg.for_info[4]} {data_len}"

    def misc_output(self):
        print("")
        output_filePath = Path(__file__).resolve().parent.parent / "output"  
        print(f"Output file saved in: {output_filePath}/domain_name.json")

    def misc_saving(self, datas, data_len, return_none_callback=None, return_data_callback=None):
        if datas:
            print(self.time_of_execution(
                msg.for_info[2], datas, return_data_callback))
            print(self.time_of_execution(
                msg.for_info[1], datas, return_none_callback, return_data_callback))
            print(self.time_of_execution(
                msg.for_info[2], datas, return_none_callback, return_data_callback))
            time.sleep(2)
            print(f"{self.time_of_execution(msg.for_info[4])}: {data_len}")
            time.sleep(1)

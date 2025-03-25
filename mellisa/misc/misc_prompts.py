import time
from datetime import datetime
from custom.log.log_custom import log_level
from misc.messages import Messages

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
        output_filePath = "/home/user/Mellisa/mellisa/mellisa/output/domain.json"
        print(f"Output file saved in: {output_filePath}")

    def misc_saving(self, datas, return_none_callback=None, return_data_callback=None):
        if datas:
            print(self.time_of_execution(
                msg.for_info[2], datas, return_data_callback))
            print(self.time_of_execution(
                msg.for_info[1], datas, return_none_callback, return_data_callback))
            print(self.time_of_execution(
                msg.for_info[2], datas, return_none_callback, return_data_callback))
            time.sleep(2)
            print(f"{self.time_of_execution(msg.for_info[4])}: {len(datas)}")
            time.sleep(1)

import time
from datetime import datetime
from custom.log.log_custom import log_level
from misc.messages import Messages
from pathlib import Path


msg = Messages()


class Misc:
    def time_of_execution(self, message, datas=None, return_none_callback=None, return_data_callback=None):
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Use different names for default callbacks to avoid parameter shadowing
        if return_data_callback is None:
            def default_data_callback(): return bool(datas)
            return_data_callback = default_data_callback
        if return_none_callback is None:
            def default_none_callback(): return not bool(datas)
            return_none_callback = default_none_callback

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

    def misc_saving(self, datas, return_none_callback=None, return_data_callback=None):
        """Log saving progress with consistent parameter handling and clearer structure."""
        if not datas:
            return
        
        # Define consistent parameters for all log calls
        log_params = {
            'datas': datas,
            'return_none_callback': return_none_callback,
            'return_data_callback': return_data_callback
        }
        
        # Log the saving process steps
        messages_to_log = [
            msg.for_info[2],  # Start saving message
            msg.for_info[1],  # Processing message  
            msg.for_info[2],  # Complete saving message
        ]
        
        for message in messages_to_log:
            print(self.time_of_execution(message, **log_params))
        
        time.sleep(2)
        
        # Log final count without callbacks (since we just need the timestamp)
        count_message = f"{self.time_of_execution(msg.for_info[4])}: {len(datas)}"
        print(count_message)
        
        time.sleep(1)

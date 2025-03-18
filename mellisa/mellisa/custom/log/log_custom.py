from misc.messages import Messages
def log_level(self, message, datas=None, return_none_cb=None, return_data_cb=None):
    log_if_found_info = "[INFO]"
    log_if_warning = "[WARNING]"

    msg = Messages()
    
    if message in msg.for_info:
        return log_if_found_info
    elif message in msg.for_warning:
        return log_if_warning
   
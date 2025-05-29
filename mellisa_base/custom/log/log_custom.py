from misc.messages import Messages


def log_level(self, message, datas=None, return_none_cb=None, return_data_cb=None):
    log_if_found_info = "\033[33m[INFO]\033[0m"
    log_if_warning = "\033[31m[WARNING]\033[0m"

    msg = Messages()

    if message in msg.for_info:
        return log_if_found_info
    elif message in msg.for_warning:
        return log_if_warning

def log(self, message=None):
    print(message)

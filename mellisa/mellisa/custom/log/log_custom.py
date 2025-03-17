def log_level(self, message, datas=None, return_none_cb=None, return_data_cb=None):
    log_if_found_info = "[INFO]"
    log_if_warning = "[WARNING]"
    
    if return_data_cb:
        return log_if_warning
    elif return_none_cb == 0:
        return log_if_warning 
    
    if message == "Scraping...":
        return log_if_found_info
    elif message == "Saving...":
        return log_if_found_info
    elif message == "PARAMETERS FOUND":
        return log_if_found_info
    elif message == "Page might not contain any parameter/s to be extracted, maybe try another one?":
        return log_if_warning
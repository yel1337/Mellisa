# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def remove_dup(data):
    return list(set(data))

class MellisaItem(scrapy.Item):
       
    item_param = scrapy.Field(
        input_processor=MapCompose(str.strip), 
        output_processor = remove_dup
    )

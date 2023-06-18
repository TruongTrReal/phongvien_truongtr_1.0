# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# items.py

import scrapy

class DemoItem(scrapy.Item):
      # define the fields for your item here like:
      name = scrapy.Field()
      pass



#make class for vietstock spider's item
class VietstockItem(scrapy.Item):
      url = scrapy.Field()
      title = scrapy.Field()
      brief = scrapy.Field()
      content = scrapy.Field()
      imgage_link = scrapy.Field()
      summarized = scrapy.Field()
      




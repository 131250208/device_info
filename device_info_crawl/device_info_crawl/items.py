# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ModelItem(scrapy.Item):
    brand_model = scrapy.Field()
    device_category = scrapy.Field()
    device_type = scrapy.Field()
    model_link = scrapy.Field()


class BrandItem(scrapy.Item):
    device_category = scrapy.Field()
    brand = scrapy.Field()


class DeviceTypeItem(scrapy.Item):
    device_category = scrapy.Field()
    device_type = scrapy.Field()

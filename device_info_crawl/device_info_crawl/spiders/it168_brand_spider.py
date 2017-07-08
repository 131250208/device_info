# -*- coding:utf8 -*-
import re

from device_info_crawl.items import *


class IT168BrandSpider(scrapy.Spider):
    name = 'IT168BrandSpider'
    allowed_domains = ['product.it168.com']
    domain = 'http://product.it168.com'
    start_urls = [
        'http://product.it168.com/afcp/0641/',
        'http://product.it168.com/afcp/0642/',
        'http://product.it168.com/afcp/0476/',
        'http://product.it168.com/0409/',
        'http://product.it168.com/wl/0412/',
        'http://product.it168.com/wl/0418/',
        'http://product.it168.com/wl/0472/',
        'http://product.it168.com/afcp/0606/',
        'http://product.it168.com/1609/',
        'http://product.it168.com/0614/',
        'http://product.it168.com/bg/0615/',
        'http://product.it168.com/bg/0105/',
        'http://product.it168.com/bg/0103/',
        'http://product.it168.com/yzsb/0618/',
        'http://product.it168.com/bg/0617/',
        'http://product.it168.com/bg/0610/',
        'http://product.it168.com/bg/0619/',
        'http://product.it168.com/bg/0608/',
        'http://product.it168.com/bg/0609/',
        'http://product.it168.com/1631/',
        'http://product.it168.com/yzsb/0604/',
        'http://product.it168.com/yzsb/0620/',
        'http://product.it168.com/yzsb/0612/',
    ]

    def parse(self, response):
        brand_item = BrandItem()
        if re.match(r'^http://product.it168.com/1609/$', response.url):
            category = response.xpath('//h1/text()').extract_first()
            brand_crawl = response.xpath('//div[@id="SingleBrand"]/dl/dd/a/text()').extract()
        else:
            category = response.xpath('//div[@class="tit4"]/text()').extract_first()
            divs = response.xpath('//div[@class="quanbu"]/div/div')
            if divs:
                brand_crawl = divs[0].xpath('div/span/a/text()').extract()
            else:
                brand_crawl = []
        if category:
            # 删除最后的"大全"二字
            category_crawl = category[:-2]
        else:
            category_crawl = ''
        brand_item['device_category'] = category_crawl
        brand_item['brand'] = brand_crawl
        yield brand_item

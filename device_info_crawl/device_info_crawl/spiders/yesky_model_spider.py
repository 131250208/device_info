# -*- coding:utf8 -*-
import re

from scrapy import Request

from device_info_crawl.items import *


class YeskyModelSpider(scrapy.Spider):
    name = 'YeskyModelSpider'
    allowed_domains = ['product.yesky.com']
    domain = 'http://product.yesky.com'
    start_urls = [
        'http://product.yesky.com/securitysystem/',
        'http://product.yesky.com/securitymonitor/',
        'http://product.yesky.com/webcamara/',
        'http://product.yesky.com/recordsystem/',
        'http://product.yesky.com/router/',
        'http://product.yesky.com/wirelessrouter/',
        'http://product.yesky.com/switchboard/',
        'http://product.yesky.com/gyjhj/',
        'http://product.yesky.com/hardwarefirewall/',
        'http://product.yesky.com/allinone/',
        'http://product.yesky.com/laserprint/',
        'http://product.yesky.com/inkprinter/',
        'http://product.yesky.com/ykdyj/',
        'http://product.yesky.com/copier/',
        'http://product.yesky.com/needleprint/',
        'http://product.yesky.com/billprint/',
        'http://product.yesky.com/rfidprint/',
        'http://product.yesky.com/assembly/',
        'http://product.yesky.com/threeddyj/',
        'http://product.yesky.com/threeddyj/',
        'http://product.yesky.com/largeformatprinter/',
        'http://product.yesky.com/labelprinter/',
        'http://product.yesky.com/labelprinter/',
    ]

    def parse(self, response):
        item = ModelItem()
        category = response.xpath('//div[@class="searchbox gray1"]/h1/a/text()').extract_first()
        if category:
            # 删除最后的"报价"二字
            category_crawl = category[:-2]
        else:
            category_crawl = ''
        next_urls = response.xpath('//a[@class="next"]/@href').extract()
        item_crawls = response.xpath('//div[@class="list blue"]')
        for item_crawl in item_crawls:
            # model_string = ''
            # model_link = ''
            brand_model_crawls = item_crawl.xpath('h2/a')
            for brand_model_crawl in brand_model_crawls:
                model_string = brand_model_crawl.xpath('text()').extract_first()
                model_link = brand_model_crawl.xpath('@href').extract_first()
                item['device_category'] = category_crawl
                item['brand_model'] = model_string
                item['device_type'] = category_crawl
                item['model_link'] = model_link
                yield item
            # 选择三种情形下的内容，此处写法需要优化
            # lis_1 = item_crawl.xpath('ul/li/text()').re(u'设备类型：(.+)')
            # lis_2 = item_crawl.xpath('ul/li/text()').re(u'产品类型：(.+)')
            # lis_3 = item_crawl.xpath('ul/li/text()').re(u'^类型：(.+)')
            # if len(lis_1) > 0:
            #     device_type_crawl = lis_1[0]
            # elif len(lis_2) > 0:
            #     device_type_crawl = lis_2[0]
            # elif len(lis_3) > 0:
            #     device_type_crawl = lis_3[0]
            # else:
            #     device_type_crawl = ''

        for next_url in next_urls:
            if re.match('[^#]+', next_url):
                yield Request(self.domain + next_url, callback=self.parse)

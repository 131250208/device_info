# -*- coding:utf8 -*-
import re
from scrapy import Request
from device_info_crawl.items import *


class IT168ModelSpider(scrapy.Spider):
    name = 'IT168ModelSpider'
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
        # 'http://product.it168.com/1609/'
    ]

    def parse(self, response):
        item = ModelItem()
        category = response.xpath('//div[@class="tit4"]/text()').extract_first()
        if category:
            # 删除最后的"大全"二字
            category_crawl = category[:-2]
        else:
            category_crawl = ''

        item_crawls = response.xpath('//div[@class="cen"]/dl')
        for item_crawl in item_crawls:
            model_string = ''
            model_link = ''
            brand_model_crawls = item_crawl.xpath('dt/a')
            for brand_model_crawl in brand_model_crawls:
                model_link = brand_model_crawl.xpath('@href').extract_first()
                model_string = brand_model_crawl.xpath('text()').extract_first()

            lis = item_crawl.xpath('.//dd/text()').extract()
            device_type_crawl = ''
            regex_list = [u'产品类型：(.+)', u'设备类型：(.+)', u'产品定位：(.+)', u'.*打印机?类型：(.+)']
            for li in lis:
                matched = False
                for regex in regex_list:
                    target_regex = re.compile(regex)
                    match_result = target_regex.match(li)
                    if match_result:
                        matched = True
                        device_type_crawl = match_result.group(1)
                        break
                if matched:
                    break
            # else:
            #     device_type_crawl = ''
            item['device_category'] = category_crawl
            if device_type_crawl == '':
                item['device_type'] = category_crawl
            else:
                item['device_type'] = device_type_crawl
            item['brand_model'] = model_string
            item['model_link'] = model_link
            yield item

        next_urls = response.xpath('//a[@class="down"]/@href').extract()
        for next_url in next_urls:
            yield Request(next_url, callback=self.parse)

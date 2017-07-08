# -*- coding:utf8 -*-
import re
from scrapy import Request
from device_info_crawl.items import *


class ZOLModelSpider(scrapy.Spider):
    name = 'ZOLModelSpider'
    allowed_domains = ['zol.com.cn']
    domain = 'http://detail.zol.com.cn'
    start_urls = [
        'http://detail.zol.com.cn/camera_equipment/',
        'http://detail.zol.com.cn/image_record/',
        'http://detail.zol.com.cn/video_server/',
        'http://detail.zol.com.cn/codec/',
        'http://detail.zol.com.cn/switches/',
        'http://detail.zol.com.cn/program-controlled_switches/',
        'http://detail.zol.com.cn/industrial_networkswitches/',
        'http://detail.zol.com.cn/router/',
        'http://detail.zol.com.cn/wireless_router/',
        'http://detail.zol.com.cn/firewall/',
        'http://detail.zol.com.cn/printer/',
        'http://detail.zol.com.cn/laser_printers/',
        'http://detail.zol.com.cn/inkjet_printers/',
        'http://detail.zol.com.cn/all-in-one_printer/',
        'http://detail.zol.com.cn/large_format/',
        'http://detail.zol.com.cn/scanner/',
        'http://detail.zol.com.cn/copier/',
        'http://detail.zol.com.cn/dye-sublimation_printer/',
        'http://detail.zol.com.cn/dot-matrix_printer/',
        'http://detail.zol.com.cn/label_printer/',
        'http://detail.zol.com.cn/card_printer/',
        'http://detail.zol.com.cn/line_printer/',
        'http://detail.zol.com.cn/barcode_printer/',
        'http://detail.zol.com.cn/3d_printer/',
        'http://detail.zol.com.cn/3d_scanner/',
        'http://detail.zol.com.cn/print_server/',
        'http://detail.zol.com.cn/printcd-rom_burner/',
        'http://detail.zol.com.cn/integration_stenograph/',
        'http://detail.zol.com.cn/cashing_machine/',
    ]

    def parse(self, response):
        item = ModelItem()
        if re.match(self.domain + '/[a-zA-Z_]+/', response.url):
            category = response.xpath('//h1/text()').extract_first()
            if category:
                # 删除最后的"报价"二字
                category_crawl = category[:-2]
            else:
                category_crawl = ''
            device_type_urls = response.xpath('//div[@id="J_ParamItem1"]//a/@href').extract()
            if len(device_type_urls) == 0:
                item_crawls = response.xpath('//div[@class="pro-intro"]')
                for item_crawl in item_crawls:
                    brand_model_crawls = item_crawl.xpath('h3/a')
                    for brand_model_crawl in brand_model_crawls:
                        model_link = brand_model_crawl.xpath('@href').extract_first()
                        model_string = brand_model_crawl.xpath('text()').extract_first()
                        if model_link:
                            link = self.domain + model_link
                        else:
                            link = ''
                        item['device_category'] = category_crawl
                        item['brand_model'] = model_string
                        item['device_type'] = category_crawl
                        item['model_link'] = link
                        yield item
                next_urls = response.xpath('//a[@class="next" or @class="historyStart"]/@href').extract()
                for next_url in next_urls:
                    yield Request(self.domain + next_url, callback=self.parse)
            else:
                for device_type_url in device_type_urls:
                    next_url = self.domain + device_type_url
                    yield Request(next_url, callback=self.parse)

        if re.match(self.domain + '/[a-zA-Z_]+/\w*\d+/?', response.url):
            category_crawl = response.xpath('//ul[@class="category-current-list clearfix"]/'
                                            'li[@class="active"]/a/text()').extract_first()
            device_type_crawl = response.xpath('//div[@id="J_ParamItem1"]/'
                                               'a[@class="active"]/text()').extract_first()
            item_crawls = response.xpath('//div[@class="pro-intro"]')
            for item_crawl in item_crawls:
                brand_model_crawls = item_crawl.xpath('h3/a')
                for brand_model_crawl in brand_model_crawls:
                    model_link = brand_model_crawl.xpath('@href').extract_first()
                    model_string = brand_model_crawl.xpath('text()').extract_first()
                    if model_link:
                        link = self.domain + model_link
                    else:
                        link = ''
                    item['device_category'] = category_crawl
                    item['brand_model'] = model_string
                    item['device_type'] = device_type_crawl
                    item['model_link'] = link
                    yield item
            next_urls = response.xpath('//a[@class="next" or @class="historyStart"]/@href').extract()
            for next_url in next_urls:
                yield Request(self.domain + next_url, callback=self.parse)

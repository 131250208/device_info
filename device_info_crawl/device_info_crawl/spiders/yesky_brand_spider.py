# -*- coding:utf8 -*-
import re

from scrapy import Request

from device_info_crawl.items import *


class YeskyBrandSpider(scrapy.Spider):
    name = 'YeskyBrandSpider'
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
        # Todo 更多品牌页面获取的设备目录是路径下的英文单词，需要采用另外的获取方式
        brand_item = BrandItem()
        brand_crawl = []
        match_result = re.match('http://product.yesky.com/list/brand/(\w+)/?', response.url)
        if match_result:
            category_crawl = match_result.group(1)
            brand_crawl_fir = response.xpath('//div[@class="rmpp jd"]/dl/dd/a/text()').extract()
            brand_crawl_sec = response.xpath('//div[@class="rmpp jd"]/ul/li/a/text()').extract()
            brand_crawl_fir.extend(brand_crawl_sec)
            brand_crawl = brand_crawl_fir
        else:
            category = response.xpath('//div[@class="searchbox gray1"]/h1/a/text()').extract_first()
            if category:
                # 删除最后的"报价"二字
                category_crawl = category[:-2]
            else:
                category_crawl = ''
            dls = response.xpath('//div[@class="searcha gray1"]//dl')
            if dls:
                brand_crawls = dls[0].xpath('dd//a')
                if len(brand_crawls) > 1:
                    more_brand = brand_crawls[-1]
                    regex = re.compile(u'更多品牌')
                    if regex.search(more_brand.xpath('text()').extract_first()):
                        more_brand_url = more_brand.xpath('./@href').extract_first()
                        if more_brand_url:
                            yield Request(more_brand_url, callback=self.parse)
                        else:
                            brand_crawl = brand_crawls.xpath('text()').extract()[1:-1]
                    else:
                        brand_crawl = brand_crawls.xpath('text()').extract()[1:]
                else:
                    brand_crawl = []
            else:
                brand_crawl = []

        brand_item['device_category'] = category_crawl
        brand_item['brand'] = brand_crawl
        yield brand_item

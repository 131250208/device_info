# -*- coding:utf8 -*-
from device_info_crawl.items import *


class ZOLDeviceTypeSpider(scrapy.Spider):
    name = 'ZOLDeviceTypeSpider'
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
        device_type_item = DeviceTypeItem()
        category = response.xpath('//h1/text()').extract_first()
        if category:
            # 删除最后的"报价"二字
            category_crawl = category[:-2]
        else:
            category_crawl = ''
        device_type_item['device_category'] = category_crawl
        device_type_item['device_type'] = response.xpath('//div[@id="J_ParamItem1"]/a/text()').extract()
        yield device_type_item

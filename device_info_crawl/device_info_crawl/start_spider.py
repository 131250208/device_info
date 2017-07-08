# -*- coding: utf-8 -*-

import os

import sys

spider_list = {'it168_brand': 'IT168BrandSpider', 'it168_device_type': 'IT168DeviceTypeSpider',
               'it168_model': 'IT168ModelSpider', 'yesky_brand': 'YeskyBrandSpider',
               'yesky_model': 'YeskyModelSpider', 'zol_brand': 'ZOLBrandSpider',
               'zol_device_type': 'ZOLDeviceTypeSpider', 'zol_model': 'ZOLModelSpider'}
result_dir = 'device_info_crawl/json_result'


def start_spider(source, target_type):
    target_spider_key = source.strip() + '_' + target_type.strip()
    if target_spider_key in spider_list.keys():
        target_spider = spider_list[target_spider_key]
        # Todo 此处直接调用命令行命令执行，后续优化可考虑是否生成线程执行
        cmd = 'scrapy crawl %s -o %s' % (target_spider, os.path.join(result_dir, target_spider_key + '.json'))
        os.system(cmd)


def start_spiders(target_list):
    # target_list是一个二元组的列表，(source, target_type)
    for ele in target_list:
        source = ele[0]
        target_type = ele[1]
        start_spider(source=source, target_type=target_type)

# Todo main函数可能错误


def main(argv):
    if isinstance(argv, list):
        start_spiders(argv)
    elif isinstance(argv, tuple):
        start_spider(argv[0], argv[1])
    else:
        print '[!] Args error !'

if __name__ == '__main__':
    main(sys.argv)

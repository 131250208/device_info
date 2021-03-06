# -*- coding: utf-8 -*-

import os
from general_util import load_json_file
import sys

spider_list = {'it168_brand': 'IT168BrandSpider', 'it168_device_type': 'IT168DeviceTypeSpider',
               'it168_model': 'IT168ModelSpider', 'yesky_brand': 'YeskyBrandSpider',
               'yesky_model': 'YeskyModelSpider', 'zol_brand': 'ZOLBrandSpider',
               'zol_device_type': 'ZOLDeviceTypeSpider', 'zol_model': 'ZOLModelSpider'}
config_file = 'device_display/static/config/scrapy_config.json'
result_dir = ''
project_dir = ''


def init_scrapy_module():
    global result_dir, project_dir
    scrapy_config_dict = load_json_file(config_file)
    if scrapy_config_dict:
        result_dir = scrapy_config_dict['result_dir']
        project_dir = scrapy_config_dict['project_dir']
        #if result_dir:
        #    os.system('cd %s; rm *.json' % result_dir)


def start_spider(source, target_type):
    target_spider_key = source.strip() + '_' + target_type.strip()
    if target_spider_key in spider_list.keys():
        target_spider = spider_list[target_spider_key]
        # Todo 此处直接调用命令行命令执行，后续优化可考虑是否生成线程执行
        rm_old_result_cmd = 'cd %s; rm %s' % (result_dir, target_spider_key + '.json')
        os.system(rm_old_result_cmd)
        cmd = 'scrapy crawl %s -o %s' % (target_spider, os.path.join(result_dir, target_spider_key + '.json'))
        open_project_dir = 'cd %s' % project_dir
        os.system('%s;%s' % (open_project_dir, cmd))
    else:
        print '[!] No this spider: %s !' % target_spider_key


def start_spiders(target_list):
    # target_list是一个二元组的列表，(source, target_type)
    # os.system('cd %s' % project_dir)
    for ele in target_list:
        source = ele[0].strip()
        target_type = ele[1].strip()
        start_spider(source=source, target_type=target_type)

# Todo main函数可能错误


def main(argv):
    init_scrapy_module()
    if isinstance(argv, list):
        start_spiders(argv)
    elif isinstance(argv, tuple):
        start_spider(argv[0], argv[1])
    else:
        print '[!] Args error !'

if __name__ == '__main__':
    main(sys.argv)

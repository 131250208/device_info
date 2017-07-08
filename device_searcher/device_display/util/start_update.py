# -*- coding: utf8 -*-

from update_info_util import update_brands, update_device_types, update_info_database, init_update_module, \
    init_current_update
from general_util import load_json_file, get_file_path

config_file = 'device_display/static/config/update_info_config.json'
data_source_name_list = ['it168_brand', 'it168_device_type', 'it168_model', 'yesky_brand', 'yesky_model', 'zol_brand',
                         'zol_device_type', 'zol_model']
data_source_dir = ''


def init_start_update_module():
    global data_source_dir
    try:
        update_config = load_json_file(config_file)
        data_source_dir = update_config['scrapy_result_dir']
    except Exception, exception:
        print '[!] Load config file：%s failed !' % config_file
        print '[!] ->', exception
    try:
        init_update_module(config_file)
    except Exception, exception:
        print '[!] Init update util failed !'
        print '[!] ->', exception


def get_data_source_file(source, target_type):
    target_file = source.strip() + '_' + target_type.strip() + '.json'
    target_file_path = get_file_path(data_source_dir, target_file)
    try:
        data_crawl_json = load_json_file(target_file_path)
    except Exception, exception:
        data_crawl_json = None
        print '[!] Load json file failed !'
        print '[!] ->', exception
    return data_crawl_json


def start_update(target_list):
    for ele in target_list:
        source = ele[0].strip()
        target_type = ele[1].strip()
        data_crawl_json = ''
        if target_type == 'brand' or target_type == 'device_type' or target_type == 'model':
            data_crawl_json = get_data_source_file(source, target_type)
            init_current_update(source + '_' + target_type)
        if data_crawl_json:
            if target_type == 'brand':
                update_brands(data_crawl_json)
            elif target_type == 'device_type':
                update_device_types(data_crawl_json)
            elif target_type == 'model':
                update_info_database(data_crawl_json)
            else:
                print '[!] Target_type error %s !' % target_type
        else:
            print '[!] Update database for (%s, %s) failed !' % (source, target_type)

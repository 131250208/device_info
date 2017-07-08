# -*- coding: utf8 -*-

from django.db.models import Q
from general_util import *
from device_display import models

BEST_MATCH = 0
STRICT_MATCH = 1

brand_crawl_name = 'brand'
device_category_crawl_name = 'device_category'
device_type_crawl_name = 'device_type'
brand_model_crawl_name = 'brand_model'
model_link_crawl_name = 'model_link'

device_category_pattern_list = [u'^\((.+)\)$', u'^（(.+)）$', u'^[^\(]+\)(.+)$', u'^[^（]+）(.+)$', u'^(.+)\(.+$',
                                u'^(.+)（.+$']
device_type_pattern_list = [u'^\((.+)\)$', u'^（(.+)）$', u'^[^\(]+\)(.+)$', u'^[^（]+）(.+)$', u'^(.+)\(.+$',
                            u'^(.+)（.+$']
brand_pattern_list = [u'^\s*\)?(.+)\(\s*$', u'^\s*\)(.+)\(?\s*$', u'^\s*）(.+)（?\s*$', u'^\s*）?(.+)（\s*$',
                      u'^\s*\((.+)\)\s*$', u'^\s*（(.+)）\s*$', u'^\s*(.+)\([^\)]+\s*$', u'^\s*(.+)（[^）]+\s*$']
model_pattern_list = [u'^\s*\)?(.+)\(\s*$', u'^\s*\)(.+)\(?\s*$', u'^\s*）(.+)（?\s*$', u'^\s*）?(.+)（\s*$',
                      u'^\s*\((.+)\)\s*$', u'^\s*（(.+)）\s*$', u'^\s*\-[^\s]*\s(.+)\s*$', u'^\s*(.+)\s[^\s]*\-\s*$',
                      u'^\s*(.+)\([^\)]+\s*$', u'^\s*(.+)（[^）]+\s*$', u'^[^\(]+\)\s*(.+)\s*$', u'^[^（]+）\s*(.+)\s*$']

model_replace_dict = {u'（': u'(', u'）': u')', u'－': u'-', u'- ': u'-', u' -': u'-'}

stop_word_list = ['a', 'an', 'the', 'of', 'off']

unknown_brand_list = []
unknown_device_type_list = []
unknown_model_list = []
not_matched_model_list = []

en_matched_cn_device_type_dict = {}

model_normalized_list = []

not_dealt_info_dir = ''
unknown_brands_file = ''
unknown_device_type_file = ''
unknown_model_file = ''
not_matched_model_file = ''

dealt_info_dir = ''
dealt_record_file = ''

current_update_name = ''

brand_list = []


def replace_abnormal_char(replace_dict, string):
    for k, v in replace_dict.items():
        string = string.replace(k, v)
    return string


def remove_special_strings(pattern_list, string):
    for pattern in pattern_list:
        regex = re.compile(pattern)
        normals = regex.search(string)
        # 是否需要用空格替换被删除的字符
        if normals:
            string = ' '.join(normals.groups()).strip()
    return string


def update_device_types(device_type_crawl_list):
    # 解决设备类型没有存入数据库的问题
    try:
        for device_type in device_type_crawl_list:
            device_category_string = device_type[device_category_crawl_name]
            device_category_removed_special = remove_special_strings(device_category_pattern_list,
                                                                     device_category_string)
            device_type_strings = device_type[device_type_crawl_name]
            for device_type_string in device_type_strings:
                device_type_removed_special = remove_special_strings(device_type_pattern_list, device_type_string)
                device_type_normalized = match_device_type(device_category_removed_special, device_type_removed_special)
                if device_type_normalized is None:
                    print '[!] Device type is not matched !'
                    print '[+] Normalizing device type ...'
                    device_type_normalized = normalize_device_type(device_category_removed_special,
                                                                   device_type_removed_special)
                    if device_type_normalized:
                        print '[+] Updating device type table ...'
                        update_device_type_table(device_type_normalized)
                    else:
                        print '[!] Device type normalization failed !'
    except Exception, exception_update_info:
        print '[!] Update device type to database exception !'
        print '[!] ->', exception_update_info


def update_brands(brand_crawl_list):
    # 解决已经匹配的品牌(大小写不同)仍然被存储进入数据库的问题
    try:
        for brand_crawl in brand_crawl_list:
            device_category_string = brand_crawl[device_category_crawl_name]
            brand_string_list = brand_crawl[brand_crawl_name]
            for brand_string in brand_string_list:
                brand_removed_special = remove_special_strings(brand_pattern_list, brand_string)
                brand_normalized = match_brand(brand_removed_special, level=STRICT_MATCH)
                if not brand_normalized:
                    print '[!] Brand is not matched !'
                    print '[+] Normalizing brand ...'
                    brand_normalized = normalize_brand(brand_removed_special)
                    if brand_normalized:
                        print '[+] Updating brand table ...'
                        update_brand_table(brand_normalized)
                    else:
                        print '[!] Brand normalization failed !'
    except Exception, exception_update_info:
        print '[!] Update brand to database exception !'
        print '[!] ->', exception_update_info


def update_info_database(info_crawl_list):
    num = 0
    total = len(info_crawl_list)
    try:
        for info_crawl in info_crawl_list:
            num += 1
            print '[+] NO.%d, Total:%d' % (num, total)
            device_category_crawl = info_crawl[device_category_crawl_name]
            device_type_crawl = info_crawl[device_type_crawl_name]
            brand_model_crawl = info_crawl[brand_model_crawl_name]
            # model_link = info_crawl[model_link_crawl_name]
            print '[+] Dealing info_crawl (%s,%s,%s) ...' % (
                device_category_crawl, device_type_crawl, brand_model_crawl)
            try:
                model_normalized = deal_info_crawl(info_crawl)
                if model_normalized:
                    print '\t[+] Model normalization finished.'
                    category = model_normalized.category
                    device_type = model_normalized.type
                    brand = model_normalized.brand
                    model = model_normalized.model

                    record = '%s,%s,%s,%s' % (category, device_type, brand, model)
                    line = '%s; %s,%s,%s' % (record, device_category_crawl, device_type_crawl, brand_model_crawl)
                    model_normalized_list.append(line)
            except Exception, exception:
                print '[!] Deal info %s; %s; %s failed !' % \
                      (device_category_crawl, device_type_crawl, brand_model_crawl)
                print '[!] ->', exception
    except Exception, exception_update_info:
        print '[!] Update info to database exception !'
        print '[!] ->', exception_update_info
    finally:
        try:
            store_file(get_file_path(dealt_info_dir, current_update_name + '_' + dealt_record_file),
                       model_normalized_list)
            print '[+] The normalized model result has been stored into file.'
            file_to_store_list = {unknown_brands_file: unknown_brand_list,
                                  unknown_device_type_file: unknown_device_type_list,
                                  unknown_model_file: unknown_model_list,
                                  not_matched_model_file: not_matched_model_list}
            for file_name, data_list in file_to_store_list.items():
                file_name = current_update_name + '_' + file_name
                store_file(get_file_path(not_dealt_info_dir, file_name), data_list)
                print '[+] The unknown file of %s has been stored.' % file_name
        except Exception, exception:
            print '[!] Store record or not_dealt file failed !'
            print '[!] ->', exception


def init_update_module(config_file):
    global not_dealt_info_dir, unknown_brands_file, unknown_device_type_file, not_matched_model_file, \
        unknown_model_file, brand_list, dealt_record_file, dealt_info_dir, current_update_name
    # father_path = os.getcwd()
    # config_file_ob_path = os.path.join(father_path, config_file)
    configs = load_json_file(config_file)
    not_dealt_info_dir = configs['not_dealt_info_dir']
    unknown_brands_file = configs['unknown_brands_file']
    unknown_device_type_file = configs['unknown_device_type_file']
    unknown_model_file = configs['unknown_model_file']
    not_matched_model_file = configs['not_matched_model_file']

    dealt_info_dir = configs['dealt_info_dir']
    dealt_record_file = configs['dealt_record_file']

    brand_list = models.Brand.objects.filter()
    if len(brand_list) == 0:
        print '[!] Brand list is not existed in database !'


def init_current_update(current_update):
    global current_update_name
    current_update_name = current_update


def deal_info_crawl(info_crawl):
    print '\t[+] Getting info_crawl ...'
    device_category_crawl = info_crawl[device_category_crawl_name]
    device_type_crawl = info_crawl[device_type_crawl_name]
    brand_model_crawl = info_crawl[brand_model_crawl_name]
    brand_crawl, model_crawl = split_brand_model_crawl(brand_model_crawl)
    model_link = info_crawl[model_link_crawl_name]
    if (device_category_crawl == '' and device_type_crawl == '') or model_crawl == '':
        return None
    print '\t[+] Removing special strings ...'
    device_category_removed_special = remove_special_strings(device_category_pattern_list, device_category_crawl)
    device_type_removed_special = remove_special_strings(device_type_pattern_list, device_type_crawl)
    brand_removed_special = remove_special_strings(brand_pattern_list, brand_crawl)
    model_removed_special = remove_special_strings(model_pattern_list, model_crawl)
    model_removed_special = replace_abnormal_char(model_replace_dict, model_removed_special)
    if (device_category_removed_special == '' and device_type_removed_special == '') or model_removed_special == '':
        return None
    print '\t[+] Matching device_type and brand ...'
    device_type_normalized = match_device_type(device_category_removed_special, device_type_removed_special)
    brand_normalized = match_brand(brand_removed_special, level=BEST_MATCH)

    if device_type_normalized is None:
        print '\t[!] Device_type is not matched !'
        print '\t[+] Normalizing device_type ...'
        device_type_normalized = normalize_device_type(device_category_removed_special, device_type_removed_special)
        if device_type_normalized:
            print '\t[+] Updating device_type table ...'
            update_device_type_table(device_type_normalized)
        else:
            print '\t[!] Device_type normalization failed !'
    if brand_normalized is None:
        print '\t[!] Brand is not matched !'
        print '\t[+] Normalizing brand ...'
        brand_normalized = normalize_brand(brand_removed_special)
        if brand_normalized:
            print '\t[+] Updating brand table ...'
            update_brand_table(brand_normalized)
        else:
            print '\t[!] Brand normalization failed !'
    print '\t[+] Matching model ...'
    model_normalized = match_model(brand_normalized, model_removed_special)
    if not model_normalized:
        print '\t[!] Model is not matched !'
        print '\t[+] Normalizing model ...'
        model_normalized = normalize_model(brand_normalized, device_type_normalized, model_removed_special, model_link)
        if model_normalized:
            print '\t[+] Updating model table ...'
            update_model_table(model_normalized)
    else:
        print '\t[+] Model is matched.'
        print '\t[+] Checking model matched result ... '
        matched = check_result(brand_normalized, device_type_normalized, model_normalized)
        if not matched:
            print '\t[!] Model matched result is unchecked !'
            print '\t[+] Adding unchecked model into not_matched_model_list ...'
            not_matched_model_list.append(info_crawl)
            print '\t[+] Inserting the unchecked model into model table ...'
            update_model_table(model_normalized)
        else:
            print '\t[+] Model matched result is checked.'
    return model_normalized


def split_brand_model_crawl(brand_model_crawl):
    brand_crawl = ''
    model_crawl = ''
    if judge_contain_cn(brand_model_crawl):
        matched = False
        pattern_fir_list = [u'^([\u4e00-\u9fa5]+)([^\u4e00-\u9fa5].*)$',
                            u'^(\w[\w\-]*)\s+[\(（]?[\u4e00-\u9fa5]+([^\u4e00-\u9fa5].*)$',
                            ]
        for pattern in pattern_fir_list:
            regex = re.compile(pattern)
            brand_model = regex.match(brand_model_crawl)
            if brand_model:
                matched = True
                brand_crawl = brand_model.group(1)
                model_crawl = brand_model.group(2)
                break
        if not matched:
            brand_crawl_regex = re.compile(u'^(\w[^\u4e00-\u9fa5]+)[\u4e00-\u9fa5].*$')
            model_crawl_regex = re.compile(u'^\w[^\u4e00-\u9fa5^\s]+\s(.+)$')
            brand = brand_crawl_regex.match(brand_model_crawl)
            model = model_crawl_regex.match(brand_model_crawl)
            if brand and model:
                brand_crawl = brand.group(1)
                model_crawl = model.group(1)
    else:
        words = brand_model_crawl.split()
        words = sorted(set(words), key=words.index)
        if len(words) > 1:
            brand_crawl = ' '.join(words[:-1])
            model_crawl = ' '.join(words[1:])
        else:
            print brand_model_crawl
    # print brand_crawl, model_crawl
    return brand_crawl, model_crawl


def match_device_type(device_category_crawl, device_type_crawl):
    if device_category_crawl == device_type_crawl:
        if judge_contain_cn(device_type_crawl):
            device_type_query_list = models.DeviceType.objects.filter(type_cn_name=device_type_crawl)
        else:
            device_type_query_list = models.DeviceType.objects.filter(type_en_name=device_type_crawl)
        if len(device_type_query_list) > 0:
            device_type_query = device_type_query_list[0]
            return device_type_query
    if (device_category_crawl, device_type_crawl) in en_matched_cn_device_type_dict.keys():
        return en_matched_cn_device_type_dict[(device_category_crawl, device_type_crawl)]
    if device_type_crawl == '':
        return None
    elif device_category_crawl == '':
        if judge_contain_cn(device_type_crawl):
            device_type_query_list = models.DeviceType.objects.filter(type_cn_name=device_type_crawl)
        else:
            device_type_query_list = models.DeviceType.objects.filter(type_en_name=device_type_crawl)
    else:
        if judge_contain_cn(device_category_crawl) and judge_contain_cn(device_type_crawl):
            device_type_query_list = models.DeviceType.objects.filter(Q(category_cn_name=device_category_crawl) &
                                                                      Q(type_cn_name=device_type_crawl))
        elif judge_contain_cn(device_category_crawl):
            device_type_query_list = models.DeviceType.objects.filter(Q(category_cn_name=device_category_crawl) &
                                                                      Q(type_en_name=device_type_crawl))
        elif judge_contain_cn(device_type_crawl):
            device_type_query_list = models.DeviceType.objects.filter(Q(category_en_name=device_category_crawl) &
                                                                      Q(type_cn_name=device_type_crawl))
        else:
            device_type_query_list = models.DeviceType.objects.filter(Q(category_en_name=device_category_crawl) &
                                                                      Q(type_en_name=device_type_crawl))
    if len(device_type_query_list) == 0:
        if judge_contain_cn(device_category_crawl):
            device_category_crawl_en = translate(device_category_crawl)
        else:
            device_category_crawl_en = device_category_crawl
        if judge_contain_cn(device_type_crawl):
            device_type_crawl_en = translate(device_type_crawl)
        else:
            device_type_crawl_en = device_type_crawl
        if device_category_crawl_en == '':
            device_type_query_list = models.DeviceType.objects.filter(type_en_name=device_type_crawl_en)
        else:
            device_type_query_list = models.DeviceType.objects.filter(Q(category_en_name=device_category_crawl_en) &
                                                                      Q(type_en_name=device_type_crawl_en))
        if len(device_type_query_list) == 0:
            device_type_query = None
        else:
            device_type_query = device_type_query_list[0]
            device_type_temp = (device_category_crawl, device_type_crawl)
            en_matched_cn_device_type_dict[device_type_temp] = device_type_query
    else:
        # 此处选择查到的结果中的第一个，通常情况下只有一个结果
        device_type_query = device_type_query_list[0]
    return device_type_query


def match_brand(brand_crawl, level):
    global brand_list
    possible_matches = []

    if level == BEST_MATCH:
        if judge_contain_cn(brand_crawl):
            for brand in brand_list:
                brand_cn = brand.cn_name
                if brand_cn and brand_cn != '' and brand_cn in brand_crawl:
                    possible_matches.append(brand)
            possible_matches.sort(key=lambda k: len(k.cn_name))
            # if len(possible_matches) > 1:
            #     print brand_crawl, possible_matches[-1].cn_name, possible_matches[-2].cn_name
        else:
            for brand in brand_list:
                brand_en = brand.en_name
                if brand_en and re.search(brand_en, brand_crawl, re.IGNORECASE):
                    possible_matches.append(brand)
            possible_matches.sort(key=lambda k: len(k.en_name))
        if len(possible_matches) > 0:
            return possible_matches[-1]
        else:
            return None
    elif level == STRICT_MATCH:
        if judge_contain_cn(brand_crawl):
            for brand in brand_list:
                brand_cn = brand.cn_name
                if brand_cn and brand_cn == brand_crawl:
                    return brand
            return None
        else:
            for brand in brand_list:
                brand_en = brand.en_name
                brand_en_regex = '^%s$' % brand_en
                if re.match(brand_en_regex, brand_crawl, re.IGNORECASE):
                    return brand
            return None
    else:
        print '[!] The level of match brand error !'


def match_model(brand_normalized, model_crawl):
    if brand_normalized is not None:
        brand = brand_normalized.en_name
        model_query_list = models.BrandModel.objects.filter(Q(brand=brand) & Q(model=model_crawl))
    else:
        print '[!] Match model failed for brand_normalized is None !'
        return None
    if len(model_query_list) == 0:
        model_query = None
    else:
        # 此处选择查到的结果中的第一个，通常情况下只有一个结果
        model_query = model_query_list[0]
    return model_query


def normalize_device_type(device_category_string, device_type_string):
    category_string_normalized, type_string_normalized = normalize_device_type_string(device_category_string,
                                                                                      device_type_string)
    if type_string_normalized != '':
        return create_device_type_object(category_string_normalized, type_string_normalized)
    else:
        deal_not_normalized('%s;%s' % (device_category_string, device_type_string), unknown_device_type_list)
        return None


def normalize_brand(brand):
    brand_string_normalized = normalize_brand_string(brand)
    if brand_string_normalized != '':
        return create_brand_object(brand_string_normalized)
    else:
        deal_not_normalized(brand, unknown_brand_list)
        return None


def normalize_model(brand_normalized, device_type_normalized, model, model_link):
    model_string_normalized = normalize_model_string(model)
    model_link_normalized = model_link.strip()
    if brand_normalized:
        brand_en = brand_normalized.en_name
        brand_cn = brand_normalized.cn_name
    else:
        brand_en = ''
        brand_cn = ''
    if device_type_normalized:
        first_type = device_type_normalized.category
        second_type = device_type_normalized.type
    else:
        first_type = ''
        second_type = ''

    if brand_normalized and model_string_normalized != '':
        return create_model_object(brand_normalized, device_type_normalized, model_string_normalized,
                                   model_link_normalized)
    else:
        deal_not_normalized('%s,%s;%s,%s;%s' % (brand_en, brand_cn, first_type, second_type, model), unknown_model_list)
        return None


def update_device_type_table(device_type):
    try:
        device_type.save()
    except Exception, exception:
        print '[!] Save device type %s failed !' % device_type.type_en_name
        print '[!] ->', exception


def update_brand_table(brand):
    global brand_list
    try:
        brand.save()
    except Exception, exception:
        print '[!] Save brand %s %s failed !' % (brand.en_name, brand.cn_name)
        print '[!] ->', exception
    brand_list = models.Brand.objects.all()


def update_model_table(model):
    try:
        model.save()
    except Exception, exception:
        print '[!] Save brand %s = %s failed !' % (model.brand, model.model)
        print '[!] ->', exception


def check_result(brand_normalized, device_type_normalized, model_normalized):
    if brand_normalized:
        if device_type_normalized:
            print '\t\t[+] Checking brand and device_type of model normalized ...'
            device_category = device_type_normalized.category
            device_type = device_type_normalized.type
            brand_en = brand_normalized.en_name
            model_brand = model_normalized.brand
            model_category = model_normalized.category
            model_type = model_normalized.device_type
            if brand_en == model_brand and device_type == model_type and device_category == model_category:
                return True
            else:
                return False
        else:
            print '\t\t[+] Checking brand of model normalized ...'
            brand_en = brand_normalized.en_name
            model_brand = model_normalized.brand
            if brand_en == model_brand:
                return True
            else:
                return False
    else:
        print '\t\t[!] Brand normalized is not existed ...'
        return False


def normalize_device_type_string(device_category_string, device_type_string):
    return device_category_string, device_type_string


def normalize_brand_string(brand_string):
    brand_string_normalized = ''
    if judge_contain_cn(brand_string):
        pattern_fir_list = [u'^\s*([\u4e00-\u9fa5]+)\s*$',
                            u'^\s*([\u4e00-\u9fa5]+)[^\u4e00-\u9fa5]+.*$',
                            u'^\s*([\w\-\s]+)[^\w\-\s]+.*[\u4e00-\u9fa5].*$']
        for pattern in pattern_fir_list:
            regex = re.compile(pattern)
            match_result = regex.match(brand_string)
            if match_result:
                brand_string_normalized = match_result.group(1)
                break
    else:
        words = brand_string.split()
        if len(words) == 1:
            brand_string_normalized = brand_string
        else:
            pattern_sec_list = [u'^\s*(\w*\d[\w\-]*)\s.*$',
                                u'^\s*(\w+\-[\w\-]*)\s.*$',
                                u'^\s*(\w+\s[^\d\-]+)\s.*$',
                                u'^\s*(\w+\s[^\d\-]+)$',
                                u'^\s*(\w+)\s+\w*[\d\-]+.*\s.*$',
                                u'^\s*(\w+)\s+\w*[\d\-]+.*$']
            for pattern in pattern_sec_list:
                regex = re.compile(pattern)
                match_result = regex.match(brand_string)
                if match_result:
                    brand_string_normalized = match_result.group(1).strip()
                    split_result = brand_string_normalized.split(' ')
                    if split_result[0].isupper():
                        brand_string_normalized = split_result[0]
                    break
    return brand_string_normalized.strip()


def normalize_model_string(model_string):
    model_string_normalized = ''
    if judge_contain_cn(model_string):
        # pattern_fir_list = [u'^\s*.+系列.*[^\w\-/](\w+[\d\-]+[\w\-\s]*)[^\w\-/\s].*$',
        #                     u'^\s*(\w+[\d\-]+[\w\-\s/\.]*)[\u4e00-\u9fa5]{0,2}型?版?\(.*[\u4e00-\u9fa5].*\)$',
        #                     u'^\s*(\w+[\d\-]+[\w\-\s/\.]*)[\u4e00-\u9fa5]{0,2}型?版?（.*[\u4e00-\u9fa5].*）$',
        #                     u'^\s*(\w+[\d\-]+[\w\-\s/\.]*)/[\u4e00-\u9fa5].*$',
        #                     u'^\s*(\w+[\d\-]+[\w\-\s/\.]*)[\u4e00-\u9fa5].*$',
        #                     u'^\s*(\w+[\w\-\s/\.]*)[\u4e00-\u9fa5]{0,2}型?版?\(.*[\u4e00-\u9fa5].*\)$',
        #                     u'^\s*(\w+[\w\-\s/\.]*)[\u4e00-\u9fa5]{0,2}型?版?（.*[\u4e00-\u9fa5].*）$',
        #                     u'^\s*(\w+[\w\-\s/\.]*)[\u4e00-\u9fa5]+$',
        #                     u'^\s*(\d[^\-]+)$',
        #                     u'^.+[^\w\-/](\w+[\d\-]+[\w\-\s/]*)[^\w\-/].*$']
        pattern_fir_list = [u'^([a-zA-Z][\w\-/\.+]*\d[\w\-/\.+]*\w\+?)\s+\d+[^\w\s+\-\.]',
                            u'^([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.+]*\w\+?)\s+\d+[^\w\s+\-\.]',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*\d[\w\-/\.+]*\w\+?)\s+\d+[^\w\s+\-\.]',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.+]*\w\+?)\s+\d+[^\w\s+\-\.]',

                            u'^([a-zA-Z][\w\-/\.+]*\d[\w\-/\.\s+]*\w\+?)\s*[^\w\s+\-\.]',
                            u'^([a-zA-Z][\w\-/\.+]*[\w\-/\.+]*\d\+?)\s*[^\w\s+\-\.]',
                            u'^([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.\s+]*\w\+?)\s*[^\w\s+\-\.]',

                            u'^([a-zA-Z][\w\-/\.+]*\d[\w\-/\.\s+]*\w\+?)\s*$',
                            u'^([a-zA-Z][\w\-/\.+]*[\w\-/\.+]*\d\+?)\s*$',
                            u'^([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.\s+]*\w\+?)\s*$',

                            u'[^\w]([a-zA-Z][\w\-/\.+]*\d[\w\-/\.\s+]*\w\+?)\s*$',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*[\w\-/\.+]*\d\+?)\s*$',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.\s+]*\w\+?)\s*$',

                            u'[^\w]([a-zA-Z][\w\-/\.+]*\d[\w\-/\.\s+]*\w\+?)\s*[^\w\s+\-\.]',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*[\w\-/\.+]*\d\+?)\s*[^\w\s+\-\.]',
                            u'[^\w]([a-zA-Z][\w\-/\.+]*\-\w[\w\-/\.\s+]*\w\+?)\s*[^\w\s+\-\.]',

                            u'^([a-zA-Z][\w\s\-\.+]*\d[\w\s\-\.+]*)[^\w\s\-\.+].*',
                            u'^([a-zA-Z][\w\s\-\.+]*\-[\w\s\-\.+]*)[^\w\s\-\.+].*',
                            u'^(\d[\w\s\-\.+]*\-[\w\s\-\.+]*)[^\w\s\-\.+].*',

                            u'^(\d[\w\-/\.\s+]+)[^\w\s\-\.+]+\s*$']
        for pattern in pattern_fir_list:
            regex = re.compile(pattern)
            search_result = regex.search(model_string)
            if search_result:
                model_string_normalized = search_result.group(1)
                break
    else:
        words = model_string.split()
        if len(words) == 1:
            model_string_normalized = model_string
        else:
            pattern_sec_list = [u'^(\d+.+)$',
                                u'^[a-zA-Z\s]+\s(\d+.+)$',

                                u'([a-zA-Z][\w\-/\.+]*\d[\w\-/\.+]*\w\+?.*)',
                                u'([a-zA-Z][\w\-/\.+]*\-[\w\-/\.+]*\w\+?.*)',
                                u'([a-zA-Z][\w\-/\.+]*\d\+?.*)',

                                u'^([a-zA-Z]+\s+\d+)']
            for pattern in pattern_sec_list:
                regex = re.compile(pattern)
                search_result = regex.search(model_string)
                if search_result:
                    model_string_normalized = search_result.group(1)
                    break
    return model_string_normalized.strip()


def remove_stop_words(stop_words, string):
    # 仅删除位于字符串开头的停用词
    for stop_word in stop_words:
        pattern = '^\s*%s\s(.*)$' % stop_word
        stop_word_regex = re.compile(pattern, re.IGNORECASE)
        match_result = stop_word_regex.match(string)
        if match_result:
            string = match_result.group(1)
            break
    return string


def create_device_type_object(category_string_normalized, type_string_normalized):
    device_category = ''
    device_type = ''
    try:
        device_category_translated = translate(category_string_normalized)
        device_type_translated = translate(type_string_normalized)
    except Exception, exception_create_device_type:
        device_category_translated = ''
        device_type_translated = ''
        print '[!] Translate device_type or device_category failed !'
        print '[!] ->', exception_create_device_type
    if judge_contain_cn(category_string_normalized):
        device_category_en = device_category_translated
        device_category_cn = category_string_normalized
    else:
        device_category_cn = device_category_translated
        device_category_en = category_string_normalized
    if judge_contain_cn(type_string_normalized):
        device_type_en = device_type_translated
        device_type_cn = type_string_normalized
    else:
        device_type_cn = device_type_translated
        device_type_en = type_string_normalized
    # 完善翻译部分，对于多个单词的采用首字母缩写，2个以下单词的不缩写。设备类型2根据单词数目确定是否缩写
    device_category_en = remove_stop_words(stop_word_list, device_category_en)
    device_type_en = remove_stop_words(stop_word_list, device_type_en)
    # device_type_en = device_type_en.replace(',', ' and')
    words = device_category_en.split(' ')
    if device_category_en and len(words) > 2:
        for word in words:
            device_category += word[0].upper()
    else:
        device_category = device_category_en
    words = device_type_en.split(' ')
    if device_type_en and len(words) > 2:
        for word in words:
            if word.isupper():
                device_type += word
            device_type += word[0].upper()
    else:
        device_type = device_type_en
    device_type_instance = models.DeviceType()
    # device_type_instance.description = ''
    device_type_instance.category_cn_name = device_category_cn
    device_type_instance.category_en_name = device_category_en
    device_type_instance.category = device_category
    device_type_instance.type_cn_name = device_type_cn
    device_type_instance.type_en_name = device_type_en
    device_type_instance.type = device_type
    return device_type_instance


def create_brand_object(brand_string_normalized):
    if judge_contain_cn(brand_string_normalized):
        pinyin_list = get_pinyin(brand_string_normalized)
        dealt_pinyin_list = []
        for i in pinyin_list:
            char_i = i[0].upper() + i[1:]
            dealt_pinyin_list.append(char_i)
        brand_en = ''.join(dealt_pinyin_list)
        brand_cn = brand_string_normalized
    else:
        # 对于英文品牌不进行中文翻译,中文名字填空
        try:
            # brand_cn = translate(brand_string_normalized)
            brand_cn = ''
        except Exception, exception_create_brand:
            brand_cn = ''
            print '[!] Translate brand_en to brand_cn failed !'
            print '[!] ->', exception_create_brand
        brand_en = brand_string_normalized
    brand_instance = models.Brand()
    brand_instance.en_name = brand_en
    brand_instance.cn_name = brand_cn
    brand_instance.country = ''
    brand_instance.product_type = ''
    brand_instance.description = ''
    brand_instance.brand_link = ''
    return brand_instance


def create_model_object(brand_normalized, device_type_normalized, model_string_normalized, model_link_normalized):
    if device_type_normalized:
        first_type = device_type_normalized.category
        second_type = device_type_normalized.type
    else:
        first_type = ''
        second_type = ''
    brand_model_instance = models.BrandModel()
    brand_model_instance.brand = brand_normalized.en_name
    brand_model_instance.category = first_type
    brand_model_instance.type = second_type
    brand_model_instance.model = model_string_normalized
    brand_model_instance.model_link = model_link_normalized
    return brand_model_instance


def deal_not_normalized(string, unknown_list):
    # 对未能识别切未能进行归一化处理的字符串进行处理，目前仅考虑将其直接加入列表中
    unknown_list.append(string)

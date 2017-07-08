# -*- coding: utf8 -*-
import json
import os
import re
import urllib
from pypinyin import lazy_pinyin


def load_json_file(file_path):
    with open(file_path, 'rb') as f:
        file_json = json.load(f)
        return file_json


def get_file_path(dir_name, file_name):
    return os.path.join(dir_name, file_name)


def store_file(file_path, data_list):
    with open(file_path, 'w+') as f:
        for data in data_list:
            if isinstance(data, str):
                f.write(data.encode('utf-8'))
                f.write('\n')
            else:
                print data


def translate(string):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&session' \
          'From=http://www.youdao.com/'
    data = {'type': 'AUTO', 'i': string.encode('utf-8'), 'doctype': 'json', 'xmlVersion': '1.8',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8', 'action': 'FY_BY_CLICKBUTTON', 'typoResult': 'true'}

    data = urllib.urlencode(data).encode('utf-8')
    response = urllib.urlopen(url, data)
    html = response.read().decode('utf-8')
    target = json.loads(html)
    string_translated = target['translateResult'][0][0]['tgt']
    return string_translated


def get_pinyin(cn_string):
    pinyin_list = lazy_pinyin(cn_string)
    return pinyin_list


def judge_contain_cn(string):
    contain_cn_regex = re.compile(u'^.*[\u4e00-\u9fa5]+.*$')
    return contain_cn_regex.match(string)


def get_levenshtein(first, second):
    if len(first) > len(second):
        first, second = second, first
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [range(second_length) for x in range(first_length)]
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    # print distance_matrix
    return distance_matrix[first_length - 1][second_length - 1]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.http import HttpResponse
from util.general_util import *
from . import models
from django.contrib import auth
from util.start_spider import init_scrapy_module, start_spiders
from util.start_update import init_start_update_module, start_update
from django.contrib.auth.decorators import login_required


# @author wycheng
# 直接获取页面的函数 --------------------------------------------------------------

# login_page
def getPage_signin(request):
    res_content = {'next': ''}
    if 'next' in request.GET:  # if there is a next_page
        if request.GET['next'] != '':
            res_content['next'] = request.GET['next']
    return render(request, 'device_display/signin.html', res_content)


# search_page
def getPage_search(request):
    # 判断登录
    if not request.user.is_authenticated():  # no login
        res_content = {'identity': 'tourist'}
    else:
        res_content = {'identity': 'admin'}

    return render(request, 'device_display/search.html', res_content)


# statistics page
def getPage_statistic(request):
    if not request.user.is_authenticated():  # no login
        res_content = {'identity': 'tourist'}
    else:
        res_content = {'identity': 'admin'}
    return render(request, 'device_display/statistics.html', res_content)


# update_page
def getPage_update(request):
    if not request.user.is_authenticated():  # no login
        res_content = {'identity': 'tourist'}
    else:
        res_content = {'identity': 'admin'}
    return render(request, 'device_display/update.html', res_content)


# managelog_page
def getPage_managelog(request):
    if not request.user.is_authenticated():  # no login
        res_content = {'identity': 'tourist'}
    else:
        res_content = {'identity': 'admin'}
    return render(request, 'device_display/managelog.html', res_content)


# search_result
def getResult_search(request):
    # identity

    identity = "admin"
    search_text = ""
    search_category = ""
    page_index = ""

    if not request.user.is_authenticated():  #if no login
        identity = 'tourist'

    # search_text
    if 'search_text' in request.POST:
        if request.POST['search_text'] != '':
            search_text = request.POST['search_text']
    # search_category
    if 'search_category' in request.POST:
        if request.POST['search_category'] != '':
            search_category = request.POST['search_category']

    if 'page_index' in request.POST:
        if request.POST['page_index'] != '':
            page_index = request.POST['page_index']

    res_content = {}
    if search_text != "" and search_category != "" and page_index != "":
        res_content = search_private(search_text, search_category, page_index)

    res_content['identity'] = identity
    res_content['search_text'] = search_text
    res_content['search_category'] = search_category
    res_content['page_index'] = page_index

    return render(request, 'device_display/search_result.html', res_content)

# def getResult_super_search(request):
#     res_content = {}
#     return render(request, 'device_display/super_search_result.html', res_content)

# wait for liumingdong
# 后端接口 -------------------------------------------------------------------------------------------------

# 临时注册接口
def signup(request):
    user = User.objects.create_user(username='wychengpublic',
                                    password='wychengpublic')
    user.save()

    user = User.objects.get(username='wychengpublic')
    if user.is_authenticated() and user.check_password("wychengpublic"):
        res_content = {"info": "signup success! your account : wychengpublic ,your pswd : wychengpublic ."}
    else:
        res_content = {"info": "failure..."}

    return render(request, 'device_display/signup_success.html', res_content)


# 登录接口
def signin(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    remember_me = request.POST.get('remember', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)

        # remember-me
        if remember_me != "true":
            request.session.set_expiry(1800)

        # Redirect to a success page.
        if request.POST['next'] != "":
            return HttpResponseRedirect(request.POST['next'])  # 跳转到点击登录前的界面
        else:
            return HttpResponseRedirect('/display/search_page/')  # 跳转到search界面
    else:
        # Show an error page
        res_content = {'status_code': 'falure', 'text': u'账号密码错误...',
                       "username_input": username, "password_input": password}
        return render(request, 'device_display/signin.html', res_content)


# 登出接口
def logout(request):
    auth.logout(request)
    next_page = request.GET['next']
    return HttpResponseRedirect(next_page)


# 搜索接口 @liumingdong
def search_private(search_text, search_category, page_index):
    # 参数： 搜索关键词/搜索分类/搜索页码
    # 分类的可选项 (字符串类型 : type/brand/model/fingerprint 类型/品牌/型号/指纹

    # 调用下层接口获取以下数据 @liumingdong
    res_content = {}
    res_content['fieldnames'] = [
        u'字段1',u'字段2',
         u'字段3',u'字段4'
    ] # 字段不包括id

    res_content['record_list'] = []
    # 查询结果的list
    for i in range(15):
        res_content['record_list'].append(
            {'id':i , 'field_val':['value', 'value2'
                , 'value4', 'value4']})

    res_content['records_num'] = 10 # 结果的总数
    res_content['page_total'] = 1 # 总页数,每页最多15条数据，不够15条也算做一页
    res_content['search_time'] = 0.134 # 查询用时（s
    return res_content

# 返回json的search
def search(request):
    search_text = request.POST['search_text']
    search_category = request.POST['search_category']
    page_index = request.POST['page_index']

    res_content = search_private(search_text,search_category,page_index)

    return HttpResponse(json.dumps(res_content))

# 删除接口 @liumingdong
def delete_record(request):
    id_list = request.POST['id_list[]']# 删除的id_list
    delete_category = request.POST['delete_category']# 删除的分类 (字符串类型 : type/brand/model/fingerprint 类型/品牌/型号/指纹

    if len(id_list) != 0:
        # 调用下层接口删除对应id的数据 @liumingdong
        pass
    res_content = {'failure':[3,6,7]}# 返回删除失败的记录的id @liumingdong
    return HttpResponse(json.dumps(res_content))

# 导出接口
def export_record(request):
    pass
# ----------------------------------------------------------------------------------------------------------------------
def index(request):
    return render(request, "device_display/index.html")


def brands_index(request):
    brands = models.Brand.objects.all()
    return render(request, 'device_display/brands_index.html', {'brands': brands})


def device_type_index(request):
    device_types = models.DeviceType.objects.all()
    return render(request, 'device_display/device_type_index.html', {'device_types': device_types})


def banner_index(request):
    banners = models.Banner.objects.all()
    return render(request, 'device_display/banner_index.html', {'banners': banners})


def search_action(request):
    # 忽略大小写查询存在问题，尤其是对某品牌下所有型号的查询
    # Todo 基于编辑距离对查询结果进行排序
    # 为品牌表中存在厂商链接的内容添加超链接
    brands = []
    brands_dealt = []
    device_types = []
    brand_models = []
    search_text = request.POST.get('search_text', '').strip()
    type_list = request.POST.get('type_list', 'brand').strip()

    search_type_dict = {'brand': '品牌', 'device_type': '类型', 'model': '型号'}
    if type_list in search_type_dict.keys():
        search_type = search_type_dict[type_list]
    else:
        search_type = 'error_type'
    records_num = 0
    if ';' in search_text or search_type == 'error_type':
        return render(request, 'device_display/search_result.html', {'brands': brands, 'device_types': device_types,
                                                                     'brand_models': brand_models,
                                                                     'search_text': search_text,
                                                                     'search_type': search_type,
                                                                     'records_num': records_num,
                                                                     })
    if type_list == 'brand':
        if judge_contain_cn(search_text):
            brands = models.Brand.objects.filter(cn_name__icontains=search_text)
        else:
            brands = models.Brand.objects.filter(en_name__icontains=search_text)
    elif type_list == 'device_type':
        if judge_contain_cn(search_text):
            device_types = models.DeviceType.objects.filter(Q(category_cn_name__icontains=search_text) |
                                                            Q(type_cn_name__icontains=search_text))
        else:
            device_types = models.DeviceType.objects.filter(Q(category__icontains=search_text) |
                                                            Q(category_en_name__icontains=search_text) |
                                                            Q(type__icontains=search_text) |
                                                            Q(type_en_name__icontains=search_text))
    else:
        brand_models = models.BrandModel.objects.filter(Q(model__icontains=search_text) |
                                                        Q(brand__icontains=search_text))
    records_num = max(len(brands), len(device_types), len(brand_models))
    return render(request, 'device_display/search_result.html', {'brands': brands, 'device_types': device_types,
                                                                 'brand_models': brand_models,
                                                                 'search_text': search_text, 'search_type': search_type,
                                                                 'records_num': records_num,
                                                                 })


def update_database(target_list):
    # Todo 将此函数规范化，并且将日志输出到文件，在对应的页面中添加更新按钮和进度条显示，点击型号列表中的品牌或类型时显示详细信息
    print '[+] Update module initiating ...'
    init_start_update_module()
    print '[+] Database updating ...'
    start_update(target_list)
    print '[+] Database update finished.'


def update_action(request):
    source_list = request.POST.getlist('source')
    target_type_list = request.POST.getlist('target_type')
    target_spider_list = []
    for source in source_list:
        for target_type in target_type_list:
            target_spider = (source, target_type)
            target_spider_list.append(target_spider)
    update_database(target_spider_list)
    return HttpResponseRedirect('/display/manage')


def scrapy_info(target_list):
    init_scrapy_module()
    start_spiders(target_list)


def scrapy_action(request):
    source_list = request.POST.getlist('source')
    target_type_list = request.POST.getlist('target_type')
    target_spider_list = []
    for source in source_list:
        for target_type in target_type_list:
            target_spider = (source, target_type)
            target_spider_list.append(target_spider)
    scrapy_info(target_spider_list)
    return HttpResponseRedirect('/display/manage')


def manage(request):
    return render(request, 'device_display/manage.html')

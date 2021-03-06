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


# managelog_page @liumingdong 8.15 修改
def getPage_managelog(request):
    res_content = {'page_total': '13', 'page_index': "1"}  # page_index是当前页码，默认为1，不必修改
    # page_total返回的是日志列表的页码总数，每页记录条数暂定为15

    if not request.user.is_authenticated():  # no login
        res_content['identity'] = 'tourist'
    else:
        res_content['identity'] = 'admin'
    return render(request, 'device_display/managelog.html', res_content)


# search_result
def getResult_search(request):
    # identity

    identity = "admin"
    search_text = ""
    search_category = ""
    page_index = ""

    if not request.user.is_authenticated():  # if no login
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


def getErrorPage_404(request):
    res_content = {"error_code": "404"}
    return render(request, 'device_display/error.html', res_content)


def getErrorPage_403(request):
    res_content = {"error_code": "403"}
    return render(request, 'device_display/error.html', res_content)


def getErrorPage_500(request):
    res_content = {"error_code": "500"}
    return render(request, 'device_display/error.html', res_content)


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
    # 分类的可选项 (字符串类型 : category/type/brand/model/fingerprint 类型/品牌/型号/指纹

    # 调用下层接口获取以下数据 @liumingdong
    res_content = {}
    res_content['fieldnames'] = [
        u'字段1', u'字段2',
        u'字段3', u'字段4'
    ]  # 字段不包括id

    # 标记是否是关联字段（修改时是否需要下拉框),与字段名对应 @liumingdong 8.24
    # 标记的可选值有['category', 'type', 'brand', 'model', 'fingerprint', 'none'],其中none为非关联字段
    res_content['relevancy'] = [
        'none', 'brand',
        'none', 'type'
    ]  # 还是要保留，这里的none对应的字段的detail是空字符串

    res_content['record_list'] = []
    # 查询结果的list
    for i in range(15):
        res_content['record_list'].append(
            {'id': i, 'field_val': ['value', 'value2'
                , 'value4', 'value4'], 'detail_list': ['', 'detail1', '', 'detail3']})  # @liumingdong 8.24

    res_content['records_num'] = 100  # 结果的总数
    res_content['page_total'] = 2  # 总页数,每页最多15条数据，不够15条也算做一页
    res_content['search_time'] = 0.134  # 查询用时（s

    res_content['res_info'] = '搜索成功' # 失败时，返回具体原因 @liumingdong 8.29
    return res_content


# 返回json的search
def search(request):
    search_text = request.POST['search_text']
    search_category = request.POST['search_category']
    page_index = request.POST['page_index']

    res_content = search_private(search_text, search_category, page_index)

    return HttpResponse(json.dumps(res_content))


# 高级搜索接口 @liumingdong 8.24
# 与普通搜索的不同之处在于 高级搜索的搜索关键词 是json格式的键值对{“字段名”：“字段值”，},前端输入示例: kk=33&&op=43
def super_search(request):
    search_text = json.loads(request.POST['search_text'])
    search_category = request.POST['search_category']
    page_index = request.POST['page_index']

    print search_text

    res_content = {}  # 返回的json格式与普通搜索的返回结果一致
    res_content['res_info'] = '搜索成功'  # 失败时，返回具体原因 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))


# 添加接口 @liumingdong 8.15
def add_record(request):
    add_category = request.POST["add_category"]
    record = request.POST["record"]  # 需要添加的record的json 字符串

    rcd_json = json.loads(record)  # key 完全对应数据库字段名

    print "add_category: %s\nrecord: %s" % (add_category, record)

    res_content = {"status": "success"}

    res_content['res_info'] = '添加成功'  # 失败时，返回具体原因 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))


# 获取国家列表 @liumingdong 8.15
def get_all_countries(request):
    res_content = {"A": [{"en_name": "America", "cn_name": "美国"}, {"en_name": "Afghanistan", "cn_name": "阿富汗"}],
                   "B": [{"en_name": "Brunei", "cn_name": "文莱"}, ], }
    return HttpResponse(json.dumps(res_content))


# 获取类别列表 @liumingdong 8.15
def get_all_categories(request):
    res_content = [{"id": "1", "name": "路由器1"},
                   {"id": "2", "name": "路由器2"},
                   {"id": "3", "name": "路由器3"},
                   {"id": "4", "name": "路由器4"},
                   {"id": "5", "name": "路由器5"},
                   {"id": "6", "name": "路由器6"},
                   {"id": "7", "name": "路由器7"},
                   {"id": "8", "name": "路由器8"},
                   {"id": "9", "name": "路由器9"}, ]
    return HttpResponse(json.dumps(res_content))


# 获取类型列表 @liumingdong 8.15
def get_types(request):
    category_id = request.POST["category_id"]
    # 根据类别 id 查找该类别下的所有类型
    res_content = [{"id": "1", "name": "XXX路由器"},
                   {"id": "2", "name": "WWW路由器"},
                   {"id": "3", "name": "YYY路由器"}, ]
    return HttpResponse(json.dumps(res_content))


# 获取品牌列表 @liumingdong 8.15
def get_brands(request):
    category_id = request.POST["category_id"]
    type_id = request.POST["type_id"]
    # 根据类别 id 和类型 id 查找所有品牌
    res_content = [{"id": "2", "name": "tp-link"}, ]
    return HttpResponse(json.dumps(res_content))


# 获取型号列表 @liumingdong 8.15
def get_models(request):
    category_id = request.POST["category_id"]
    type_id = request.POST["type_id"]
    brand_id = request.POST["brand_id"]
    # 根据类别 id 、类型 id 和品牌 id 查找所有型号
    res_content = [{"id": "2", "name": "型号名称"}, ]
    return HttpResponse(json.dumps(res_content))


# 删除接口 @liumingdong
def delete_record(request):
    # 修正了传参方式为传递json字符串 @liumingdong 8.29
    id_list = json.loads(request.POST['id_list'])  # 删除的id_list
    delete_category = request.POST['delete_category']  # 删除的分类 (字符串类型 : type/brand/model/fingerprint 类型/品牌/型号/指纹

    if len(id_list) != 0:
        # 调用下层接口删除对应id的数据 @liumingdong
        pass
    res_content = {'failure': [3, 6, 7]}  # 返回删除失败的记录的id @liumingdong
    res_content['res_info'] = '部分选项删除失败了,...'  # 有失败选项时，返回具体原因 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))


# 修改接口
def edit_record(request):
    # 修正了传参方式为传递json字符串 @liumingdong 8.29
    row_list = json.loads(request.POST['row_list'])  # 要修改的行数据的list，第一个字段为id
    delete_category = request.POST['delete_category']  # 删除的分类 (字符串类型 : type/brand/model/fingerprint 类型/品牌/型号/指纹

    # 进行后台的修改操作 @liumingdong

    res_content = {'sucess': [[0, '字段1', '字段2', '字段3', '字段4'],
                              [1, '字段1', '字段2', '字段3', '字段4'], ]}  # 返回修改成功的元组的list，包括id在内的所有字段为一个元组,@liumingdong

    res_content['failure'] = [2,3,4]
    res_content['res_info'] = '部分选项修改失败了,...'  # 有失败选项时，返回具体原因 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))


# 导出接口
# @liumingdong 8.29 导出接口用GET方法传递参数
def export_record(request):
    search_text = request.GET['search_text']
    search_category = request.GET['search_category']

    print search_text
    print search_category

    res_content = {"status": "success"}
    return HttpResponse(json.dumps(res_content))


# 接口，获取网站爬虫更新的源网站列表 @liumingdong 8.15
def get_srcweb_list(request):
    # circle的可选值：[“1个月”， “2个月”， “3个月”， “6个月”， “1年”]
    res_content = [{"id": "1", "name": "中关村在线", "website": "http://www.zol.com.cn/", "cycle": "2"},
                   {"id": "2", "name": "中关村不在", "website": "http://www.woc.com.cn/", "cycle": "6"}]  # @liumingdong 8.24
    return HttpResponse(json.dumps(res_content))


# 接口，获取更新记录列表 @liumingdong 8.15
def get_updrcd_list(request):
    page = request.GET["page"]

    res_content = [{"id": "1", "data_src_name": "中关村在线", "upd_time": "2017-10-3 15:44:56",
                    "type_num": "132", "brand_num": "44", "model_num": "345"},
                   {"id": "2", "data_src_name": "xxx文件名", "upd_time": "2017-10-3 15:42:56",
                    "type_num": "34", "brand_num": "345", "model_num": "111"}, ]
    return HttpResponse(json.dumps(res_content))


# 修改源网站更新周期的接口 @liumingdong 8.15
def adjust_upd_circle(request):
    web_id = request.POST["web_id"]
    new_circle = request.POST["new_circle"]  # circle参数的值有["1", "2", "3", "6", "12"]，
    # 对应[“1个月”， “2个月”， “3个月”， “6个月”， “1年”]

    res_content = {"status": "success"}

    res_content["res_info"] = "修改周期成功" # 如果修改失败，返回具体原因。 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))


# 更新回退操作接口 @liumingdong 8.15
def recall_upd(request):
    upd_id_list_str = request.POST["upd_id_list_str"]
    upd_id_list_json = json.loads(upd_id_list_str)  # 获取的是一个id_list，里面存有需要回退的所有更新记录的id

    res_content = {"status": "success"}
    return HttpResponse(json.dumps(res_content))


# 获取操作管理日志的接口 @liumingdong8.15
def get_manage_log(request):
    page = request.GET["page_index"]

    res_content = [{"opt_time": "2017-10-3 15:44:56", "opt_user": "admin", "opt_brief": "添加了一条记录......",
                    "opt_detail": "记录详情"},
                   {"opt_time": "2017-10-3 15:44:56", "opt_user": "admin", "opt_brief": "添加了一条记录......",
                    "opt_detail": "记录详情"}, ]

    if page == "2":
        res_content = [{"opt_time": "2019-10-3 15:44:56", "opt_user": "admin", "opt_brief": "添加了一条记录......",
                        "opt_detail": "记录详情"},
                       {"opt_time": "2018-10-3 15:44:56", "opt_user": "admin", "opt_brief": "添加了一条记录......",
                        "opt_detail": "记录详情"}, ]
    return HttpResponse(json.dumps(res_content))


# 上传并导入文件的接口 @liumingdong 8.22
def upload_file(request):
    num_files = len(request.FILES)
    for index in range(num_files):
        file = request.FILES['upl_file_' + str(index)]
        name = file.name
        with open('./upd_files/' + name + '.txt', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    # 上传文件完毕，这里可以做一些导入文件到数据库的处理 @liumingdong 8.22

    # 上传完毕重新跳转上传文件页面
    res_content = {}

    if not request.user.is_authenticated():  # no login
        res_content['identity'] = 'tourist'
    else:
        res_content['identity'] = 'admin'

    res_content["res_info"] = "文件导入成功"  # 如果导入失败，返回具体原因。 @liumingdong 8.29

    return render(request, 'device_display/update.html', res_content)


# 网站爬取更新下的立即更新功能的接口 @liumingdong 8.29
def update_immediately(request):
    website_id_list = json.loads(request.POST['website_id_list'])
    print website_id_list

    res_content = {"status": "success"}

    res_content["res_info"] = "网站爬取更新成功"  # 如果更新失败，返回具体原因。 @liumingdong 8.29
    return HttpResponse(json.dumps(res_content))

# 获取能力展示的柱状图数据 @liumingdong 8.29
def get_capacity(request):
    res_content = [
        {'能力方向': '型号', '总量': 1523, '品牌数量': 1523},
        {'能力方向': '指纹', '总量': 1223, '品牌数量': 1523},
    ]
    return HttpResponse(json.dumps(res_content))


# 获取能力展示的型号对应品牌的饼图数据 @liumingdong 8.29
def get_brands_model(request):
    res_content = [
        {'brand_name': '品牌1', 'num': 1523},
        {'brand_name': '品牌2', 'num': 1223},
        {'brand_name': '品牌3', 'num': 2123},
        {'brand_name': '品牌4', 'num': 4123},
        {'brand_name': '品牌5', 'num': 3123},
        {'brand_name': '品牌6', 'num': 7123}
    ]
    return HttpResponse(json.dumps(res_content))

# 获取能力展示的指纹识别的饼图数据 @liumingdong 8.29
def get_brands_fingerprint(request):
    res_content = [
        {'brand_name': '品牌1', 'num': 1523},
        {'brand_name': '品牌2', 'num': 1223},
        {'brand_name': '品牌3', 'num': 2123},
        {'brand_name': '品牌4', 'num': 4123},
        {'brand_name': '品牌5', 'num': 3123},
        {'brand_name': '品牌6', 'num': 7123}
    ]
    return HttpResponse(json.dumps(res_content))

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

# -*- coding: utf-8 -*-
"""device_searcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^brands_index/$', views.brands_index, name='brands_index'),
    url(r'^device_type_index/$', views.device_type_index, name='device_type_index'),
    url(r'^banner_index/$', views.banner_index, name='banner_index'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^update/$', views.update_action, name='update_action'),
    url(r'^scrapy/$', views.scrapy_action, name='scrapy_action'),

    # -----------------------------------------------------------------------------------------------
    # 直接获取页面url
    url(r'^signin_page/$', views.getPage_signin, name='getPage_signin'),
    url(r'^search_page/', views.getPage_search, name='getPage_search'),
    url(r'^update_page/$', views.getPage_update, name='getPage_update'),
    url(r'^statistics_page/$', views.getPage_statistic, name='getPage_statistic'),
    url(r'^managelog_page/$', views.getPage_managelog, name='getPage_managelog'),
    url(r'^search_result_page/$', views.getResult_search, name='getResult_search'),
    url(r'^error_page_404/$', views.getErrorPage_404, name='error_page'),
    url(r'^error_page_403/$', views.getErrorPage_403, name='error_page'),
    url(r'^error_page_500/$', views.getErrorPage_500, name='error_page'),
    # url(r'^super_search_result_page/$', views.getResult_super_search, name='getResult_super_search'),

    # ----------------------------------------------------------------------------------------------
    # 接口
    url(r'^signup/', views.signup),  # signup
    url(r'^signin/', views.signin, name='signin'),  # login
    url(r'^logout/', views.logout, name='logout'),  # logout
    url(r'^search/', views.search, name='search'),  # search
    url(r'^add_record/', views.add_record, name='add_record'),  # edit_record
    url(r'^edit_record/', views.edit_record, name='edit_record'),  # edit_record
    url(r'^delete_record/', views.delete_record, name='delete_record'),  # delete_record
    url(r'^export_record/', views.export_record, name='export_record')  # export_record
]

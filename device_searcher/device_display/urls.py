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
    url(r'^search_result/$', views.search_action, name='search_action'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^update/$', views.update_action, name='update_action'),
    url(r'^scrapy/$', views.scrapy_action, name='scrapy_action'),
]
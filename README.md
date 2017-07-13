# 项目简介
## 1. 功能
    自动化更新设备品牌/类型/型号数据库
## 2. 数据来源
    网络/上传文件/人工
## 3. 结构
    device_info_crawl为爬虫模块，自动从网络爬取数据
    device_searcher为管理及数据处理模块，提供管理功能
    sqls目录下为数据库建表文件及历史遗留数据
## 4. 框架
    爬虫模块使用scrapy，管理模块使用django，数据库使用mysql
## 5. 版本
    python 2.7.6
    scrapy 1.4.0
    django 1.11.3
    mysql 5.6.33
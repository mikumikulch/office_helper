#!/usr/bin/python3
# -*- coding:utf-8 -*-
import gzip
import json
import logging
import ssl
import time
import urllib
from http import cookiejar
from urllib import request, parse
from datetime import datetime, timedelta

from attendance_spider import HttpConfig

"""
'利信员工考勤信息抓取蜘蛛'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__author__ = 'Chuck Lin'


class LixinStaffInfoSpider(object):
    # 用于获取 cookie 设置的请求用请求头
    __head_for_get_cookie = HttpConfig.head_for_get_cookie
    # 用于获取请求头参数
    __head_for_get_attendance_data = HttpConfig.head_for_get_attendance_data

    # __post_data = {"date": "2017-6", "staffid": "6590415"}

    def __ungzip(self, data):
        try:  # 尝试解压
            # print('正在解压.....')
            data = gzip.decompress(data)
            # print('解压完毕!')
        except:
            pass
        # print('未经压缩, 无需解压')
        return data

    def get_opener(self, head, openner=None):
        cookie = cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor()
        # gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        if openner is None:
            opener = urllib.request.build_opener(handler)
        header = []
        # 字典转换为truple集合.
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    def reset_cookies(self, head, openner):
        header = []
        # 字典转换为truple集合.
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        openner.addheaders = header
        return openner

    def get_staff_info(self, openner, url='https://kaoqin.bangongyi.com/attend/index/record?_=1498544871927'):
        ssl._create_default_https_context = ssl._create_unverified_context
        now = datetime.now()
        yesterday_month = now - timedelta(days=1)
        formated_month = now.strftime('%Y-%m')
        post_data = {"date": formated_month, "staffid": "6590415"}
        post_data = parse.urlencode(post_data).encode()
        response = openner.open(url, post_data)
        # request = urllib.request.Request(self.request_url, post_data, headers=LixinStaffInfoSpider.head)
        # 通过openner发送请求
        # response = urllib.request.urlopen(request)
        print(self.__ungzip(response.read()).decode('utf-8'))
        return

    def get_staff_cookie(self, openner,
                         url='https://kaoqin.bangongyi.com/attend/index/index?corpid=wx7a3ce8cf2cdfb04c&t=3'):
        ssl._create_default_https_context = ssl._create_unverified_context
        openner.open(url)
        return

    def query_staff_attendance_info(self):
        openner = self.get_opener(self.__head_for_get_cookie)
        self.get_staff_cookie(openner)
        openner_with_staff_cookie = self.reset_cookies(self.__head_for_get_attendance_data, openner)
        self.get_staff_info(openner_with_staff_cookie)


lixin_info_spider = LixinStaffInfoSpider()
lixin_info_spider.query_staff_attendance_info()
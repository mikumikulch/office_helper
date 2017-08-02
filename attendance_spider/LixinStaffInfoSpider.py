#!/usr/bin/python3
# -*- coding:utf-8 -*-
import gzip
import logging
import ssl
import urllib
from datetime import datetime, timedelta
from http import cookiejar
from urllib import request, parse

import HelperConfig

"""
'利信员工考勤信息抓取'
"""

__author__ = 'Chuck Lin'

logger_name = 'office_helper'
logger = logging.getLogger(logger_name)

class LixinStaffInfoSpider(object):
    # 用于获取 cookie 设置的请求用请求头
    __head_for_get_cookie = HelperConfig.head_for_get_cookie
    # 用于获取请求头参数
    __head_for_get_attendance_data = HelperConfig.head_for_get_attendance_data

    def __init__(self) -> None:
        super().__init__()

    # __post_data = {"date": "2017-6", "staffid": "6590415"}



    def __ungzip(self, data):
        try:  # 尝试解压
            # print('正在解压.....')
            data = gzip.decompress(data)
            # print('解压完毕!')
        except:
            logger.error('解压响应数据发生异常，跳过解压处理')
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
        logger.debug('根据 cookiee 信息请求考勤记录')
        ssl._create_default_https_context = ssl._create_unverified_context
        now = datetime.now()
        # 如果今天是月初，则获取上一个月的数据。
        yesterday_month = now - timedelta(days=1)
        if now.day == 1:
            formated_month = yesterday_month.strftime('%Y-%m')
        else:
            formated_month = now.strftime('%Y-%m')
        post_data = {"date": formated_month, "staffid": "6590415"}
        post_data = parse.urlencode(post_data).encode()
        response = openner.open(url, post_data)
        # request = urllib.request.Request(self.request_url, post_data, headers=LixinStaffInfoSpider.head)
        # 通过openner发送请求
        # response = urllib.request.urlopen(request)
        ungzip_response = self.__ungzip(response.read()).decode('utf-8')
        logger.debug(ungzip_response)
        logger.debug('请求考勤记录成功')
        return ungzip_response

    def get_staff_cookie(self, openner,
                         url='https://kaoqin.bangongyi.com/attend/index/index?corpid=wx7a3ce8cf2cdfb04c&t=3'):
        logger.debug('请求考勤主页面，尝试获取 cookie 信息')
        ssl._create_default_https_context = ssl._create_unverified_context
        openner.open(url)
        logger.debug('获取 cookie 信息成功')
        return

    def query_staff_attendance_info(self):
        openner = self.get_opener(self.__head_for_get_cookie)
        self.get_staff_cookie(openner)
        openner_with_staff_cookie = self.reset_cookies(self.__head_for_get_attendance_data, openner)
        return self.get_staff_info(openner_with_staff_cookie)

#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
根据配置文件获取相应用户的考勤日志与记录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

__author__ = 'Chuck Lin'

import gzip
import logging
import ssl
import urllib
from datetime import datetime, timedelta
from urllib import request, parse

from attendance_spider import HelperConfig

logger_name = 'office_helper'
logger = logging.getLogger(logger_name)

"""
'利信员工考勤信息抓取'
"""

__author__ = 'Chuck Lin'


class LixinStaffInfoSpider(object):
    # 用于获取 cookie 设置的请求用请求头
    __head_for_get_cookie = HelperConfig.head_for_get_cookie
    # 用于获取请求头参数
    __head_for_get_attendance_data = HelperConfig.head_for_get_attendance_data

    def __init__(self) -> None:
        super().__init__()

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
        """
        创建一个具备自动处理 cookie 功能的 http openner 模块
        若 openner 不为空，则重新为 openner 设置 header 信息
        :param head: dict 类型
        :param openner: urllib.openner
        :return:openner
        """
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
        """
        获取员工的当月考勤信息数据。如果今天是月初，则获取上一个月的数据。
        :param openner: http openner
        :param url: 固定链接
        :return: 本月考勤 json 数据
        """
        logger.info('根据 cookiee 信息请求考勤记录')
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
        logger.info('请求考勤记录成功')
        return ungzip_response

    def get_staff_cookie(self, openner,
                         url='https://kaoqin.bangongyi.com/attend/index/index?corpid=wx7a3ce8cf2cdfb04c&t=3'):
        """
        获取员工对应的最新 session、以进行后续处理.
        :param openner: 组装好基本参数的 http urllib 模块对象
        :param url: 固定的获取最新 session 的链接
        :return: 获取到最新 session 信息并设置到 cookie 的 http openner 对象
        """
        logger.info('请求考勤主页面，尝试获取 cookie 信息')
        ssl._create_default_https_context = ssl._create_unverified_context
        openner.open(url)
        logger.info('获取 cookie 信息成功')
        return

    def query_staff_attendance_info(self):
        openner = self.get_opener(self.__head_for_get_cookie)
        self.get_staff_cookie(openner)
        openner_with_staff_cookie = self.reset_cookies(self.__head_for_get_attendance_data, openner)
        return self.get_staff_info(openner_with_staff_cookie)

    def get_server_time(self, openner,
                        url='https://kaoqin.bangongyi.com/attend/check/get-time?v=1506595896876&_=1506595896882'):
        """
        获取 session 对应的服务器时间
        :param openner:
        :param url: 固定的获取服务器时间的链接
        :return:当前服务器时间的 epoch time
        """
        logger.info('获取 session 对应的服务器时间')
        ssl._create_default_https_context = ssl._create_unverified_context
        response = openner.open(url)
        ungzip_response = self.__ungzip(response.read()).decode('utf-8')
        logger.info('session 对应的服务器时间为 %s ' % ungzip_response)
        return ungzip_response

    def check_clocktime_and_location(self, openner, clocktime, url='https://kaoqin.bangongyi.com/attend/check'):
        """
        检查终端坐标与服务器打卡时间是否满足要求
        :param openner: openner
        :param clocktime: 打卡时间（服务器时间）
        :return:json 数组
        example
                {
                "data": {
                    "url": "\/attend\/check\/success?device_id=34128&device_type=0&date=2017-09-30&userid=6590415"
                },
                "errno": 0,
                "errmsg": "ok"
                }
        """
        logger.info('向服务器确认打卡信息是否满足要求')
        request_data = parse.urlencode({'validityTime': clocktime, 'device_type': '0',
                                        'lat': '30.637487771874', 'lng': '104.07350944463',
                                        'device_id': '34128'}).encode()
        response = openner.open(url, request_data)
        ungzip_response = self.__ungzip(response.read()).decode('utf-8')
        logger.debug('打卡信息确认完毕。%s' % ungzip_response)
        return ungzip_response

    def cheat(self, openner, clocktime):
        """
        向服务器发送打卡请求，实现打卡
        :param openner:  openner
        :param clocktime: 打卡时间
        :return: html 页面
        """
        now_date = datetime.now().strftime('%Y-%m-%d')
        logger.info('向服务器发送打卡请求，打卡日期 %s 打卡时间 %s' % (now_date, clocktime))
        url = 'https://kaoqin.bangongyi.com/attend/check/success?device_id=34128&device_type=0&date=%s&userid=6590415' % now_date
        openner.open(url)
        logger.info('打卡完毕。打卡日期 %s 打卡时间 %s' % (now_date, clocktime))

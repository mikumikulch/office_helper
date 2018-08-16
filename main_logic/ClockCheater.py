#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
自动打卡小助手核心程序
负责调用其他模块完成任务
"""
import json
import logging
from datetime import datetime

from attendance_spider import HelperConfig
from attendance_spider.StaffInfoSpider import StaffInfoSpider

__author__ = 'Chuck Lin'

logger_name = 'office_helper'
logger = logging.getLogger(logger_name)


class ClockCheater(object):
    # 用于获取 cookie 设置的请求用请求头
    __head_for_get_cookie = HelperConfig.head_for_get_cookie
    # 用于获取请求头参数
    __head_for_get_attendance_data = HelperConfig.head_for_get_attendance_data

    def __init__(self) -> None:
        super().__init__()

    def engin_start(self):
        # 获取用户当前最新 session 并且保存到 cookie 中
        openner = StaffInfoSpider.get_opener(self.__head_for_get_cookie)
        StaffInfoSpider.get_staff_cookie(openner)
        # 获取当前 session 的对应服务器时间
        server_time = StaffInfoSpider.get_server_time(openner)
        # 根据获取到的服务器时间，检查坐标与时间
        check_result = StaffInfoSpider.check_clocktime_and_location(openner, server_time)
        # 判断检查结果
        check_result_json = json.load(check_result)
        errmsg = check_result_json['errmsg']
        if errmsg != 'ok':
            logger.error('坐标与日期检查出现异常 errmsg %s server_time %s ，处理结束' % (check_result, server_time))
            return
        # 发送打卡请求。打卡时间为当前日期 + sessin 对应的服务器时间
        StaffInfoSpider.cheat(openner, server_time)
        logger.info('自动打卡成功。打卡时间：%s' % datetime.fromtimestamp(server_time))


robot = ClockCheater()
# 最初版本脚本周6或者周7目前是不运行的，暂不支持休息日加班。
now = datetime.now()
logger.info('自动打卡开始。当前时间： %s' % now)
# TODO 节假日不运行脚本
if now.weekday() is 5 or now.weekday() is 6:
    logger.info('当前日期是周6或者周日，不运行脚本。')
else:
    robot.engin_start()

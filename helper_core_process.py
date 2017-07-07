#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
'利信小助手核心程序'
"""
import json

import logging

from attendance_spider.LixinStaffInfoSpider import LixinStaffInfoSpider
from datetime import datetime, timedelta, time

__author__ = 'Chuck Lin'


class HelperRobot(object):
    def __init__(self) -> None:
        super().__init__()

    def compare_date(self, element):
        attendence_date = datetime.fromtimestamp(element).strftime('%Y-%m-%d')
        # 昨日的日期
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        formated_yesterday = yesterday.strftime('%Y-%m-%d')
        return formated_yesterday == attendence_date

    def engin_start(self):
        # 抓取当月考勤记录
        lixin_info_spider = LixinStaffInfoSpider()
        staff_attendance_info_json = json.loads(lixin_info_spider.query_staff_attendance_info())
        # 获取当月考勤记录的 dict 数据
        attendance_dict = staff_attendance_info_json['data']['checkDay']
        # 获取记录的日期数据列表
        check_day_list = [k for k, v in attendance_dict.items()]
        # 过滤出考勤日期中不是昨日的日期的数据
        int_check_day_list = list(map(lambda x: int(x), check_day_list))
        yesterday_attendance_date = list(filter(self.compare_date, int_check_day_list))[0]
        # 获取打卡记录
        checkin_attr_dict = attendance_dict[str(yesterday_attendance_date)][0]['checkout_attr']
        checkout_attr_dict = attendance_dict[str(yesterday_attendance_date)][0]['checkout_attr']
        try:
            checkout_time = datetime.strptime(checkout_attr_dict['time'], '%H:%M:%S')
        except BaseException:
            logging.error('您的退勤打卡时间有异常。请确认您的打卡信息。退勤打卡时间：%s', checkout_attr_dict['time'])
            return
        # 判断打卡时间是否超过8点。如果超过8点，调用打印系统打印加班单。
        criterion_time = datetime(1900, 1, 1, 20, 0, 0)
        if checkout_time >= criterion_time:
            # 当天符合加班标准，调用打印机模块
            pass
        else:
            yesterday = datetime.fromtimestamp(yesterday_attendance_date).strftime('%Y-%m-%d')
            logging.info('您昨日的考勤时间 %s 未满足加班条件。程序处理结束', yesterday)


robot = HelperRobot()
robot.engin_start()

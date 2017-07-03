#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
'利信小助手核心程序'
"""
import json

from attendance_spider.LixinStaffInfoSpider import LixinStaffInfoSpider
from datetime import datetime, timedelta, time

__author__ = 'Chuck Lin'


class HelperRobot(object):
    def __init__(self) -> None:
        super().__init__()

    def compare_date(self, element):
        attendence_date = datetime.fromtimestamp(element).strftime('%Y-%m-%d')
        # 昨日的日期
        now = datetime.now
        yesterday = now - timedelta(days=1)
        formated_yesterday = yesterday.strftime('%Y-%m-%d')
        return formated_yesterday is attendence_date

    def engin_start(self):
        # 抓取当月考勤记录
        lixin_info_spider = LixinStaffInfoSpider()
        staff_attendance_info_json = json.loads(lixin_info_spider.query_staff_attendance_info())
        # 获取当月考勤记录的 dict 数据
        attendance_dict = staff_attendance_info_json['data']['checkDay']
        # 获取记录的日期数据列表
        check_day_list = [k for k in attendance_dict.items()]
        # 过滤出考勤日期中不是昨日的日期的数据
        yesterday_attendance_date = filter(self.compare_date, map(lambda x: float(x), check_day_list))[0]
        # 获取打卡记录
        checkin_attr_dict = attendance_dict[yesterday_attendance_date]['checkin_attr']
        checkout_attr_dict = attendance_dict[yesterday_attendance_date]['checkout_attr_dict']
        # TODO trycatch 处理转换异常，未打卡时表示请假或者缺勤，处理结束
        checkout_time = time.strftime(checkout_attr_dict['time'], '%H:%M:%S')


robot = HelperRobot()
robot.engin_start()

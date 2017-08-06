#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
'利信小助手核心程序'
"""
import json
import logging
from logging.handlers import RotatingFileHandler

from attendance_spider.LixinStaffInfoSpider import LixinStaffInfoSpider
from make_document import overTimeHelper
from datetime import datetime, timedelta


logger_name = 'office_helper'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
#最多备份5个日志文件，每个日志文件最大10M，当最新内容超出限度后将会覆盖最旧的内容
Rthandler = RotatingFileHandler('make_document/attandence.log', maxBytes=10*1024*1024,backupCount=5)
fh = logging.FileHandler('make_document/attandence.log', encoding='utf8')
fh.setLevel(logging.INFO)

fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(Rthandler)

__author__ = 'Chuck Lin'


class HelperRobot(object):
    def __init__(self) -> None:
        super().__init__()

    def compare_date(self, element):
        attendence_date = datetime.fromtimestamp(element).strftime('%Y-%m-%d')
        # 昨日的日期
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        if yesterday.weekday() is 5:
            yesterday = yesterday - timedelta(days=1)
        elif yesterday.weekday() is 6:
            yesterday = yesterday - timedelta(days=2)
        else:
            pass
        formated_yesterday = yesterday.strftime('%Y-%m-%d')
        # print('昨天%s是星期%s' % (formated_yesterday, yesterday.weekday()))
        return formated_yesterday == attendence_date

    # noinspection PyTypeChecker
    def engin_start(self):
        logger.info('开始抓取昨日考勤记录')
        # 抓取当月或者上一个月考勤记录
        lixin_info_spider = LixinStaffInfoSpider()
        staff_attendance_info_json = json.loads(lixin_info_spider.query_staff_attendance_info())
        # 获取当月考勤记录的 dict 数据
        attendance_dict = staff_attendance_info_json['data']['checkDay']
        # 获取记录的日期数据列表
        check_day_list = [k for k, v in attendance_dict.items()]
        # 过滤出考勤日期中不是昨日的日期的数据
        int_check_day_list = list(map(lambda x: int(x), check_day_list))
        # 因为是月初，所以获取到的考勤日期只包括8月1日，所以无法过滤出昨日的数据，需要获取7月份的考勤日期。
        yesterday_attendance_date = list(filter(self.compare_date, int_check_day_list))[0]
        # 获取打卡记录
        checkin_attr_dict = attendance_dict[str(yesterday_attendance_date)][0]['checkout_attr']
        checkout_attr_dict = attendance_dict[str(yesterday_attendance_date)][0]['checkout_attr']
        try:
            checkout_time = datetime.strptime(checkout_attr_dict['time'], '%H:%M:%S')
        except BaseException:
            logger.error('您的退勤打卡时间有异常。请确认您的打卡信息。退勤打卡时间：%s', checkout_attr_dict['time'])
            return
        criterion_time = datetime(1900, 1, 1, 20, 0, 0)
        if checkout_time >= criterion_time:
            logger.info('考勤记录抓取完毕，昨日加班时间超过8点，调用加班助手填写加班审批单')
            # 判断打卡时间是否超过8点。如果超过8点，调用打印系统打印加班单。
            overTimeHelper.write_document(datetime.fromtimestamp(int(checkout_attr_dict['date'])), checkout_time)
        else:
            yesterday = datetime.fromtimestamp(yesterday_attendance_date).strftime('%Y-%m-%d')
            logger.info('您昨日的考勤时间 %s 未满足加班条件。程序处理结束', yesterday)
            logger.info('利信办公小助手机器人运行结束')


logger.info('利信办公小助手机器人运行开始')
robot = HelperRobot()
# 最初版本脚本周6或者周7目前是不运行的，暂不支持休息日加班。
now = datetime.now()
if now.weekday() is 5 or now.weekday() is 6:
    logger.info('当前日期是周6或者周日，不运行脚本。')
else:
    robot.engin_start()

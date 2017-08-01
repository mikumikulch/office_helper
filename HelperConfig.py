#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
自定义化配置信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# 用于获取 cookie 设置的请求用请求头
head_for_get_cookie = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, '
                  'like Gecko) Mobile/13F69 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN ',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-cn',
    'accept': '*',
    'cookie': 'bangongyiuser100133043=lincanhan%7C%7C%7Cd1f8a13f9e009019fcc4015f66ddb9ab; '
              'gr_user_id=9f179084-328b-452a-95f5-0825d8f257a9'
}

# 用于获取请求头参数
head_for_get_attendance_data = {
    # ':method': 'GET',
    # ':schema': 'https',
    # ':authority': 'kaoqin.bangongyi.com',
    'accept': '*/*',
    'connection': 'keep-alive',
    'user-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, '
                  'like Gecko) Mobile/13F69 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN',
    'referer': 'https://kaoqin.bangongyi.com/attend/index/record',
    'accept-Language': 'zh-CN,zh;q=0.8',
    'accept-Encoding': 'gzip, deflate'
}

# 加班单的保存路径
overtime_save_path = '/Users/lincanhan/Documents/工作资料/利信资料/利信流程与制度文档/加班审批表'

# 加班人姓名
user_name = '林灿涵'

# 发送邮件用账户
from_addr_and_user = 'lincanhan@lixin360.com'
# 发件邮箱登录密码
email_password = 'NtC7j25fXDicYKhL'
# 发件服务器
smtp_server = 'smtp.exmail.qq.com'
# 收件人账户
to_addr = 'lincanhan@lixin360.com'

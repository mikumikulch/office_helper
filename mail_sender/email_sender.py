# -*- coding:utf-8 -*-
# 敏感词360 林灿涵


"""
邮件发送模块
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

__author__ = 'Chuck Lin'

import logging
import smtplib
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from attendance_spider import HelperConfig

# 设置发件人账户与密码，发件服务器，收件人账户
logger_name = 'office_helper'
logger = logging.getLogger(logger_name)

from_addr_and_user = HelperConfig.from_addr_and_user
password = HelperConfig.email_password
to_addr =  HelperConfig.to_addr
smtp_server = HelperConfig.smtp_server


def send_mail(mail_title, attachment_path, file_name):
    msg = MIMEMultipart()
    from_name = from_addr_and_user
    to_name = to_addr
    # msg['From'] = Header(from_name, 'utf-8')
    # msg['To'] = Header(to_name, 'utf-8')
    msg['From'] = from_name
    msg['To'] = to_name
    msg['Subject'] = Header(mail_title, 'utf-8').encode()
    msg.attach(MIMEText('本邮件由机器人自动发送.有问题请联系发件人', 'plain', 'utf-8'))

    fp = open(attachment_path, 'rb')
    att = MIMEText(fp.read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
    # 此处的 encode 不能要，不然会出现收到的 word 打不开有非法字符的问题。
    # encoders.encode_base64(att)
    msg.attach(att)

    # with open(attachment_path, 'rb') as f:
    #     # 设置附件的MIME和文件名，这里是file类型:
    #     mime = MIMEBase('file', 'xls', filename=file_name)
    #     # 加上必要的头信息:
    #     mime.add_header('Content-Disposition', 'attachment', filename=file_name)
    #     mime.add_header('Content-ID', '<0>')
    #     mime.add_header('X-Attachment-Id', '0')
    #     # 把附件的内容读进来:
    #     mime.set_payload(f.read())
    #     # 用Base64编码:
    #     encoders.encode_base64(mime)
    #     # 添加到MIMEMultipart:
    #     msg.attach(mime)

    try:
        logger.info('开始发送邮件到用户')
        # server = smtplib.SMTP(smtp_server)
        server = smtplib.SMTP_SSL(smtp_server)
        server.set_debuglevel(1)
        server.login(from_addr_and_user, password)
        server.sendmail(from_addr_and_user, [to_addr], msg.as_string())
        logger.info('邮件发送成功')
        server.quit()
    except smtplib.SMTPException as e:
        logger.error("Error: 邮件发送失败", e)

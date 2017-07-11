#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
' 自动填写加班单、并保存到对应文件目录中。
最后发送回邮件到邮箱、提示打印。打印功能也许可以用 applescript+pages 实现？'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from docx import Document
from docx.shared import Inches

document = Document()


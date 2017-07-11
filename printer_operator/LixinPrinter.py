#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 获取利信用户考勤数据。

"""
' 自动打印用户文件到远程打印机'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


__author__ = 'Chuck Lin'

import cups



conn = cups.Connection()
printers = conn.getPrinters()

for printer in printers:
    print(printer, printers[printer]["device-uri"])





if __name__ == '__main__':
    pass

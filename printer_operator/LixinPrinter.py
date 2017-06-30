#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 获取利信用户考勤数据。

"""
' 自动打印用户文件到远程打印机'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
是的你可以试试

"""

__author__ = 'Chuck Lin'

from PyQt5.QtPrintSupport import QPrinter

printer = QPrinter()
printer.setOutputFileName('test.pdf')
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setPageSize(QPrinter.A4)
printer.setFullPage(True)

# printer.webview.print_(printer)


if __name__ == '__main__':
    pass

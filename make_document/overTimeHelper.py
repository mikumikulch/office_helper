#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
' 自动填写加班单、并保存到对应文件目录中。
最后发送回邮件到邮箱、提示打印。打印功能也许可以用 applescript+pages 实现？'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from datetime import datetime

import docx
from docx.oxml.ns import qn
from docx.shared import Pt

doc = docx.Document('/Users/lincanhan/Desktop/加班审批表.docx')
style = doc.styles['Normal']
style.font.name = u'宋体'
style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

# 备用符号 ☑

def reset_form_date_paragraphs():
    # 获取填表日期段落
    form_date_paragraphs = doc.paragraphs[1]
    form_date_paragraphs.clear()
    now = datetime.now()

    mutipart_date = '填表日期:%d年%d月%d日' % (now.year, now.month, now.day)
    run = form_date_paragraphs.add_run(mutipart_date, 'Default Paragraph Font')
    # run.font.name = u'宋体'
    # r = run._element
    # r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    run.font.size = Pt(10)
    doc.save('/Users/lincanhan/Desktop/加班审批表.docx')
    print(doc.paragraphs[1].runs[0].text)


def reset_base_info(checkout_date, checkout_time):
    def set_tables_fontsize(x):
        x.style.font.size = Pt(11)
        return x

    pre_tables = [table for table in doc.tables]
    tables = list(map(set_tables_fontsize, pre_tables))
    # 填写加班事由 TODO 自动爬取近期的需求，
    tables[0].rows[1].cells[2].text = '真量贷中新需求开发与系统遗留 bug 修正'
    # 填写申请人
    tables[0].rows[0].cells[1].text = '林灿涵'
    # 填写所在部门
    tables[0].rows[0].cells[3].text = '信息技术部门'
    tables[0].rows[0].cells[5].text = '程序员'
    # 填写加班类型
    # TODO 根据加班时间的不同，填入不同的加班类型
    tables[0].rows[4].cells[2].text = '☑ 延时加班    □ 休息日加班    □ 法定节假日加班'
    # 申请加班时间
    year, month, day, hour = checkout_date.year, checkout_date.month, checkout_date.day, checkout_time.hour
    apply_work_time = '%d 年 %d 月 %d 日  19 时 至  %d 年 %d  月  %d 日  %d 时' % (year, month, day, year, month, day, hour)
    tables[0].rows[5].cells[2].text = apply_work_time
    # TODO 按照固定格式填写加班模板表。
    doc.save('/Users/lincanhan/Desktop/加班审批表.docx')


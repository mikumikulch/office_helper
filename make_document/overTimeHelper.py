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

# 备用符号 ☑
# print(len(doc.paragraphs[0].runs))
# print(doc.paragraphs[0].text)


def reset_form_date_paragraphs():
    # 获取填表日期段落
    form_date_paragraphs = doc.paragraphs[1]
    form_date_paragraphs.clear()
    # form_date_run = form_date_paragraphs.runs[0]
    # text = form_date_paragraphs.runs[0].text
    # italic = form_date_paragraphs.runs[0].italic
    # print(text)
    # print(italic)
    now = datetime.now()

    mutipart_date = '填表日期:%d年%d月%d日' % (now.year, now.month, now.day)
    # form_date_run.clear()
    # form_date_run.text = mutipart_date
    run = form_date_paragraphs.add_run(mutipart_date, 'Default Paragraph Font')
    run.font.name = u'宋体'
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    run.font.size = Pt(10)
    doc.save('/Users/lincanhan/Desktop/加班审批表.docx')
    print(doc.paragraphs[1].runs[0].text)


def reset_base_info_():
    # form_date_paragraphs = doc.paragraphs[2]
    tables = [table for table in doc.tables]
    # for table in tables[0]:
    print(len(tables[0].rows))
    tables[0].rows[1].cells[2].text = '测试'
    tables[0].rows[1].cells[2].paragraphs[0].runs[0].font.size = Pt(10)
    #TODO 按照固定格式填写加班模板表。
    for row in tables[0].rows:
        print(len(row.cells))
        for cell in row.cells:
            print(cell.text)
            # doc.save('/Users/lincanhan/Desktop/加班审批表.docx')
            # print(form_date_paragraphs.runs[0].text)  # reset_form_date_paragraphs()
    doc.save('/Users/lincanhan/Desktop/加班审批表.docx')

reset_form_date_paragraphs()
reset_base_info_()

# print(doc.paragraphs[1].text)
# print(doc.paragraphs[2].text)

# fullText = []
# for para in doc.paragraphs:
#     fullText.append(para.text)

# print(fullText)

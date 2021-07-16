# -*- coding: utf-8 -*-
"""
批量输入 Maya 路径 | 最后一个路径为 Excel 输出路径
通过 xlwt 模块输出 Excel 统计数据

|------|----------|---------|---------|----------|------|
| 编号 |  文件路径 | 动画名称 | 骨骼数量 | 动画帧数 | 合计 |
|------|----------|---------|---------|----------|------|
|      |          |         |         |          |      |
|------|----------|---------|---------|----------|------|

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-01 09:24:04'

from maya import cmds
import xlwt
import sys
import os
import maya.standalone as std
std.initialize()


book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('骨骼统计', cell_overwrite_ok=True)
font = xlwt.Font()
font.name = '微软雅黑'

alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER

style = xlwt.XFStyle()
style.font = font
style.alignment = alignment

sheet.write(0, 0, u"编号", style)
sheet.write(0, 1, u"文件路径", style)
sheet.write(0, 2, u"动画名称", style)
sheet.write(0, 3, u"骨骼数量", style)
sheet.write(0, 4, u"动画帧数", style)
sheet.write(0, 5, u"合计", style)

err_list = []

# print(sys.argv)

for i, file_name in enumerate(sys.argv[1:-1], 1):

    sheet.write(i, 0, i, style)
    sheet.write(i, 1, file_name, style)
    sheet.write(i, 2, os.path.basename(file_name), style)

    if not os.path.exists(file_name):
        for j in range(3, 6):
            sheet.write(i, j, u"文件路径不存在", style)
        # err_list.append('%s - file not exists' % file_name)
        continue

    # NOTE 打开文件
    cmds.file(file_name.replace('\\',"/"), f=1, open=1)

    if not cmds.objExists("*:root"):
        for j in range(3, 6):
            sheet.write(i, j, u"root骨骼不存在", style)
        # err_list.append('%s - cannot find the root bone' % file_name)
        continue

    jnt_count = len(cmds.ls("*:root", dag=1, ni=1, fl=1, type="joint"))
    min_frame = cmds.playbackOptions(q=1, min=1)
    max_frame = cmds.playbackOptions(q=1, max=1)
    total_frame = max_frame - min_frame

    sheet.write(i, 3, jnt_count, style)
    sheet.write(i, 4, total_frame, style)
    sheet.write(i, 5, jnt_count*total_frame, style)

    print("sheet",sheet)

output_directory = sys.argv[-1]
book.save(output_directory)
os.startfile(os.path.dirname(output_directory))

# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 16:47:16'

"""
https://www.liaoxuefeng.com/wiki/897692888725344/926177394024864
"""

import os
DIR = os.path.dirname(__file__)

# 导入SQLite驱动:
import sqlite3
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect(os.path.join(DIR,'test.db'))
# 创建一个Cursor:
cursor = conn.cursor()
# 执行一条SQL语句，创建user表:
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 继续执行一条SQL语句，插入一条记录:
cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
# 通过rowcount获得插入的行数:
cursor.rowcount
1
# 关闭Cursor:
cursor.close()
# 提交事务:
conn.commit()
# 关闭Connection:
conn.close()

# import sqlite3
# conn = sqlite3.connect(os.path.join(DIR,'test.db'))
# cursor = conn.cursor()
# # 执行查询语句:
# cursor.execute('select * from user where id=?', ('1',))
# # 获得查询结果集:
# values = cursor.fetchall()
# print (values)
# cursor.close()
# conn.close()
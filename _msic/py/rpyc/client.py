#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import rpyc


conn = rpyc.connect('localhost',9999)
#调用服务器端的方法，格式为：conn.root.xxx。xxx代表服务器端的方法名
# get_time是服务端的那个以"exposed_"开头的方法
result = conn.root.close()
print (result)

conn.close()
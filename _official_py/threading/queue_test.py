# -*- coding: utf-8 -*-
"""
http://c.biancheng.net/view/2624.html
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-26 14:20:06'


import threading
import time
import queue
def product(bq):
    str_tuple = ("Python", "Kotlin", "Swift")
    for i in range(3):
        print(threading.current_thread().name + "生产者准备生产元组元素！")
        time.sleep(0.2)
        # 尝试放入元素，如果队列已满，则线程被阻塞
        bq.put(str_tuple[i % 3])
        print(threading.current_thread().name \
            + "生产者生产元组元素完成！")
def consume(bq):
    while True:
        print(threading.current_thread().name + "消费者准备消费元组元素！")
        time.sleep(0.2)
        # 尝试取出元素，如果队列已空，则线程被阻塞
        t = bq.get()
        print(threading.current_thread().name \
            + "消费者消费[ %s ]元素完成！" % t)
# 创建一个容量为1的Queue
bq = queue.Queue(maxsize=1)
# 启动3个生产者线程
threading.Thread(target=product, args=(bq, )).start()
threading.Thread(target=product, args=(bq, )).start()
threading.Thread(target=product, args=(bq, )).start()
# 启动一个消费者线程
threading.Thread(target=consume, args=(bq, )).start()
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
import os
import signal
from rpyc import Service
from rpyc.utils.server import ThreadedServer


class TimeService(Service):
    # 对于服务端来说， 只有以"exposed_"打头的方法才能被客户端调用，所以要提供给客户端的方法都得加"exposed_"
    def exposed_get_time(self):
        return time.ctime()  # time模块中的一个内置方法

    def exposed_close(self):
        print("run close")
        os._exit(0)

s = ThreadedServer(
    service=TimeService, hostname="localhost", port=9999, auto_register=False
)
s.start()

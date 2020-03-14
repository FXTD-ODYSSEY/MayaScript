# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 10:27:56'

"""

"""

import sys
import ctypes
import platform
import threading
import multiprocessing
from cefpython3 import cefpython as cef

from functools import partial

import socket
from rpyc import Service  
from rpyc.utils.server import ThreadedServer  

# from PySide.QtGui import *
# from PySide.QtCore import *

class CefServer(ThreadedServer):
    def __init__(self,*args,**kwargs):
        self.cef = kwargs.get("cef")
        del kwargs["cef"]
        super(CefServer,self).__init__(*args,**kwargs)


    def accept(self):
        """accepts an incoming socket connection (blocking)"""
        # super(RefServer,self).accept()
        while self.active:
            self.cef.MessageLoopWork()
            try:
                sock, addrinfo = self.listener.accept()
            except socket.timeout:
                pass
            except socket.error:
                ex = sys.exc_info()[1]
                if get_exc_errno(ex) in (errno.EINTR, errno.EAGAIN):
                    pass
                else:
                    raise EOFError()
            else:
                break

        if not self.active:
            return

        sock.setblocking(True)
        self.logger.info("accepted %s with fd %s", addrinfo, sock.fileno())
        self.clients.add(sock)
        self._accept_method(sock)


class TestService(Service):  
    cef = None
    browser = None

    def exposed_test(self,arg):
        return cef

    def exposed_urlEvent(self):
        self.cef.LoadUrl(r"https://www.bilibili.com/")
        return self.cef

    def exposed_createBrowser(self, winId):  
        print self.ret
    
    def exposed_timerEvent(self):
        self.cef.MessageLoopWork()
        
    def exposed_resizeEvent(self, winId):  
        winId = int(winId)
        self.cef.WindowUtils.OnSize(winId, 0, 0, 0)

if __name__ == "__main__":
    print "run server"

    windowInfo = cef.WindowInfo()
    windowInfo.SetAsChild(int(sys.argv[1]))


    settings = {}
    settings["context_menu"] = {
        "enabled": False,
        "navigation": False,  # Back, Forward, Reload
        "print": False,
        "view_source": False,
        "external_browser": False,  # Open in external browser
        "devtools": False,  # Developer Tools
    }
    cef.Initialize(settings)

    browser = cef.CreateBrowserSync(windowInfo,url="https://www.baidu.com")
    TestService.cef = cef
    TestService.browser = browser
    sr = CefServer(TestService, port=int(sys.argv[2]), auto_register=False,cef=cef)  
    sr.start()  
    


    

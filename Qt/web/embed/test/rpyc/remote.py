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

import rpyc
from rpyc import Service  
from rpyc.utils.server import ThreadedServer  

global resize
resize = False
global url
url = None
class TestService(Service):  
    url = None

    def exposed_onResizeCall(self):
        global resize
        resize = True
        return resize

    def exposed_resizeCall(self):  
        global resize
        if resize:
            resize = False
            return True

    def exposed_onLoadUrl(self,_url):
        global url
        url = _url

    def exposed_loadUrl(self):
        global url
        if url:
            _url = url
            url = None
            return _url

def createBrowser():
    winId = int(sys.argv[1])
    windowInfo = cef.WindowInfo()
    windowInfo.SetAsChild(winId)


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

    port = int(sys.argv[2])
    conn = rpyc.connect('localhost',port)  
    while True:
        url = conn.root.loadUrl()
        if url and url != browser.GetUrl():
            browser.LoadUrl(url)
        elif conn.root.resizeCall():
            cef.WindowUtils.OnSize(winId, 0, 0, 0)
        cef.MessageLoopWork()


    cef.Shutdown()

if __name__ == "__main__":

    sr = ThreadedServer(TestService, port=int(sys.argv[2]), auto_register=False)  

    p = multiprocessing.Process(target=createBrowser)
    p.start()  

    sr.start()
    


    

# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 10:27:56'

"""

"""

from cefpython3 import cefpython as cef
import platform
import sys

import threading
import multiprocessing

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = multiprocessing.Process(sec, func_wrapper)
    t.start()

def main():
    winId = sys.argv[1]
    windowInfo = cef.WindowInfo()

    # print cef
    # print dir(cef)
    # print windowInfo
    # print dir(windowInfo)

    windowInfo.SetAsChild(int(winId))

    settings = {}
    settings["browser_subprocess_path"] = "%s/%s" % (
        cef.GetModuleDirectory(), "subprocess")
    settings["context_menu"] = {
        "enabled": False,
        "navigation": False,  # Back, Forward, Reload
        "print": False,
        "view_source": False,
        "external_browser": False,  # Open in external browser
        "devtools": False,  # Developer Tools
    }
    cef.Initialize(settings)
    
    # # browser = cef.CreateBrowserSync(url="https://www.baidu.com",
    browser = cef.CreateBrowserSync(windowInfo,url="https://www.baidu.com",
                          window_title="Hello World!")

    print browser
    print dir(browser)
    # # print browser.GetWindowHandle()
    # # print dir(browser.GetWindowHandle())

    # cef.WindowUtils.OnSize(int(winId), 0, 0, 0)
    # set_interval(lambda: cef.WindowUtils.OnSize(int(winId), 0, 0, 0),.2)
    
    while True:
        # time.sleep(0.1)
        cef.MessageLoopWork()

    cef.Shutdown()

if __name__ == '__main__':
    main()
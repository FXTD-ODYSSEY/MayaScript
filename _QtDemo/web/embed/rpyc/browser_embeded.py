# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 10:27:56'

"""

"""

from cefpython3 import cefpython as cef
import platform
import sys


def main():
    winId = sys.argv[1]
    windowInfo = cef.WindowInfo()
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
    
    cef.CreateBrowserSync(windowInfo,url="https://www.baidu.com",
                          window_title="Hello World!")
    
    # cef.MessageLoop()
    # cef.Shutdown()

if __name__ == '__main__':
    main()
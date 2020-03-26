# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 10:27:56'

"""

"""

import sys
import platform
from cefpython3 import cefpython as cef

from rpyc import Service  
from rpyc.utils.server import ThreadedServer  
      
class TestService(Service):  
    
    def exposed_test(self,arg):
        print arg
        return cef

    def exposed_createBrowser(self, winId):  
        winId = int(winId)
        cef.Initialize()
        windowInfo = cef.WindowInfo()
        windowInfo.SetAsChild(winId)

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
        
        cef.CreateBrowserSync(windowInfo,
                            url="https://www.baidu.com",
                            window_title="Hello World!")

        return cef
        # cef.MessageLoop()
        # cef.Shutdown()
    
    def exposed_timerEvent(self):
        cef.MessageLoopWork()
        
    def exposed_resizeEvent(self, winId):  
        winId = int(winId)
        cef.WindowUtils.OnSize(winId, 0, 0, 0)

if __name__ == "__main__":
    print "run server"
    sr = ThreadedServer(TestService, port=int(sys.argv[1]), auto_register=False)  
    sr.start()  

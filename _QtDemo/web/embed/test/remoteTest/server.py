# coding:utf-8  
      
from rpyc import Service  
from rpyc.utils.server import ThreadedServer  
      
class TestService(Service):  
      
    # 对于服务端来说， 只有以"exposed_"打头的方法才能被客户端调用，所以要提供给客户端的方法都得加"exposed_"  
    def exposed_test(self, num):  
        return 1+num  
      
sr = ThreadedServer(TestService, port=9999, auto_register=False)  
sr.start()  
# coding:utf-8  

import rpyc  
      
# 参数主要是host, port  
conn =rpyc.connect('localhost',9999)  
# test是服务端的那个以"exposed_"开头的方法  
cResult =conn.root.test(11)  
print (cResult)
conn.close()  
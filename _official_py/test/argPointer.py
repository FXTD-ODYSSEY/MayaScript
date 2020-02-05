# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-03 17:42:33'

"""
# NOTE 实现参数修改效果
a = 1
b = 1

def increment(a,b):
    a += 1
    b += 1

increment(a,b)
print a,b 
# NOTE 打印 2,2
"""

# TODO -------------------------------------------------------------------------

def pointer(func):
    def wrapper(*args,**kwargs):

        point_list = []
        point_list.extend(list(args))
        point_list[0] = 3
        print point_list
        arg = func(*args,**kwargs)
        return arg
        
    return wrapper

a = 1
b = 1

@pointer
def increment(a,b):
    a += 1
    b += 1

increment(a,b)
print a,b 

class debugState(object):
    def __init__(self):
        super(debugState,self).__init__()

a = debugState()

print dir(a)



# TODO -------------------------------------------------------------------------

"""
# NOTE 数组方案
a = [1,2,3]
def testFunc(a):
    a.append(4)
    a[1] = a[1] + 1
    print dir(a)
    print "nested",a

testFunc(a)
print a

"""

"""
# NOTE 字典方案
data = {1:"a"}
def modifyDict(data):
    data[1] = 3

print data
modifyDict(data)
print data
"""




# from decorator import decorator

# @decorator
# def pass_through(wrapped, instance=1, *args, **kwargs):
#     print(instance,args,kwargs)
#     return wrapped(*args, **kwargs)


# def function(a):
#     pass

# function.test = 1
# function = pass_through(function)
# print(dir(function))
# function(a=1)

import wrapt

class Test(object):

    @wrapt.decorator
    def deco(func,instance,args,kwargs):
        print(instance,func)
        print("validate",args)
        return func(*args,**kwargs)

    @deco
    def write(self,rel_item):
        print('write')
        
    @deco
    @staticmethod
    def write_static(rel_item):
        print('write_static')

test = Test()
test.write('asd')
test.write_static('asd')

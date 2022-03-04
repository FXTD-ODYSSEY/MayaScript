from multipledispatch import dispatch


@dispatch(int, int)
def add(x, y):
    print("plus")
    return x + y


@dispatch(object, object)
def add(x, y):
    return "%s + %s" % (x, y)


# @dispatch(int, bool)
# def add(x, y):
#     return "int bool"


@dispatch(int)
def add(x, y=2):
    return "int bool"


res = add(1, 2)
print(res)

res = add(1, "hello")
print(res)

res = add(1, True)
print(res)

res = add(1)
print(res)


# res = map(lambda v:str(v),[1,2,3],[True,False])
# print(res)

class TestObject(object):
        
    @dispatch(int)
    def test(self,x):
        print("int")
    
    @dispatch(bool)
    def test(self,x):
        print("boolean")
    
    @dispatch(float)
    @classmethod
    def test(cls,x):
        print("float")
    

test = TestObject()
test.test(1)
test.test(True)
test.test(1.0)
    

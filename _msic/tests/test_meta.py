class Friendly(object):
    def hello(self):
        print ('Hello')

class Person(object): pass

p = Person()
Person.__bases__ = (Friendly,)
p.hello()  # prints "Hello"
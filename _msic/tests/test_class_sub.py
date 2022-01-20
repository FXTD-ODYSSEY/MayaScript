
class Parent(object):
    pass

a = Parent()
b = Parent()

for i in Parent.__subclasses__():
    
    print(i)


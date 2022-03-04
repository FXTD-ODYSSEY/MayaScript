import time
from dependencies import Injector
from conf import test




def baz():
    time.sleep(test)

def bar():
    baz()

def foo():
    bar()

def main():
    foo()
    
if __name__ == '__main__':
    main()
    
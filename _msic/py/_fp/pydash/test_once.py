from pydash import py_

class Test(object):
    
    def __init__(self):
        self.run = py_.once(self.run)
    
    def run(self):
        print("run")

test = Test()
test.run()
test.run()
test.run()

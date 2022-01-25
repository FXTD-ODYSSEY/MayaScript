
import os
import imp
DIR = os.path.dirname(__file__)
pluggy_test = os.path.join(DIR,"pluggy_test.py")
pluggy_test = imp.load_source("test",pluggy_test)

print(pluggy_test)


print(type("Base",(pluggy_test,),{}))


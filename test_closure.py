
def main(test='das'):
    a = test
    b = 'bcc'
    callback = lambda : "%s : %s" % (a,b)
    callback = lambda : "{} : {}".format(a,b)
    return callback

callback = main()

# print(dir(callback))

# func_closure = callback.func_closure 
# func_code = callback.__code__ 
# func_defaults = callback.func_defaults 
# func_dict = callback.func_dict 

code = callback.__code__ 
closure = callback.__closure__ 

# print ("co_argcount",code.co_argcount)
# print ("co_cellvars",code.co_cellvars)
# print ("co_code",code.co_code)
# print ("co_consts",code.co_consts)
# print ("co_filename",code.co_filename)
# print ("co_firstlineno",code.co_firstlineno)
# print ("co_flags",code.co_flags)
# print ("co_freevars",code.co_freevars)
# print ("co_kwonlyargcount",code.co_kwonlyargcount)
# print ("co_lnotab",code.co_lnotab)
# print ("co_name",code.co_name)
# print ("co_names",code.co_names)
# print ("co_nlocals",code.co_nlocals)
# print ("co_posonlyargcount",code.co_posonlyargcount)
# print ("co_stacksize",code.co_stacksize)
# print ("co_varnames",code.co_varnames)
# print ("replace",code.replace)

for c in closure:
    print(c.cell_contents)
    break

# print(closure)
# code = code.co_code


['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_posonlyargcount', 'co_stacksize', 'co_varnames', 'replace']

['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']

['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__'] 
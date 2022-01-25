from decorator import decorator

@decorator
def pass_through(wrapped, instance=1, *args, **kwargs):
    print(instance,args,kwargs)
    return wrapped(*args, **kwargs)


def function(a):
    pass

function.test = 1
function = pass_through(function)
print(dir(function))
function(a=1)
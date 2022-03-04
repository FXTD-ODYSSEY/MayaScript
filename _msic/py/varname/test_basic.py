from varname import varname
def wrapped():
    return function()

def function():
    # retrieve the variable name at the 2nd frame from this one
    return varname(frame=2)

func = wrapped() # func == 'func'

print([func])


import deal

@deal.pre(lambda a, b: a >= 0 and b >= 0)
# @deal.raises(ZeroDivisionError)  # this function can raise if `b=0`, it is ok
def div(a, b):
    return a / b

div(-1,-2)


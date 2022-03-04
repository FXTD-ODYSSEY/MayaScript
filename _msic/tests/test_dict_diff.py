import copy

a = {
    1: {
        1: {
            1: 1,
            2: 2,
        }
    }
}
_a = copy.deepcopy(a)
b = {
    1: {
        1: {
            1:1,
        },
        2: {}
    }
}





def merge(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge(d1[k], d2[k])
        else:
            d1[k] = d2[k]   
merge(a,b)
print(a)
print(_a)
print(a == _a)

import itertools
from itertools import chain 

for attribute,axis in chain.from_iterable(itertools.product('trs','xyz')):
    print(attribute,axis)



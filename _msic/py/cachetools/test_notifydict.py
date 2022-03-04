from addict import Dict
from blinker import signal,Signal

on_notify = Signal()

def notify(method):
    def decorator(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        
        on_notify.send(self)
        return result
    return decorator

class NotifyDict(dict):
    
    __delitem__ = notify(dict.__delitem__)
    __setitem__ = notify(dict.__setitem__)
    clear = notify(dict.clear)
    pop = notify(dict.pop)
    popitem = notify(dict.popitem)
    setdefault = notify(dict.setdefault)
    update =  notify(dict.update)
    
class TestDict(Dict,NotifyDict):
    @on_notify.connect
    def _on_change(self, name):
        print(name,"on change")

a = TestDict()
a.test =1 
a.test =2

del a.test

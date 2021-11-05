print("load dev")
import module_test.model.base as base


class DevBase(base.ModelBase):
    def __init__(self):
        super(DevBase, self).__init__()


def dev_call():
    base.base_call()
    print("dev_call")
    print(DevBase())


class DevTest(DevBase):
    pass


from module_test.controller.mvc import mvc
from module_test.model import carry

class CaseMVC(mvc.DevMVC):
    pass

def carry_call():
    print(carry)
    print(carry.carry_all())
    print("asd")
    print("CaseMVC", CaseMVC)
    print('carry_call')

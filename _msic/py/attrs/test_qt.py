import attr
from Qt import QtWidgets
from dayu_widgets.qt import application


@attr.s
class TestAttr(object):
    data = attr.ib(type=dict, factory=dict)
    parent = attr.ib(default=lambda:"name")
    parser = attr.ib(default=None)
    def __attrs_post_init__(self):
        super(TestAttr,self).__init__()

class AttrButton(TestAttr,QtWidgets.QPushButton):
    name = property(lambda self: "{0}_0".format(self.item_type))
    
    # item_type = attr.ib(type=str)
    def __init__(self,*args, **kwargs):
        super(AttrButton, self).__init__(*args, **kwargs)


with application():
    button = AttrButton()
    print(button.parser)
    button.show()

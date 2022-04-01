import attr

@attr.s(init=False)
class ItemAttr(object):
    name = property(lambda self: "{0}_0".format(self.item_type))
    
    item_type = attr.ib(type=str)
    data = attr.ib(type=dict, factory=dict)
    parent = attr.ib(default=lambda:"name")
    parser = attr.ib(default=None)

    def __init__(self):
        super(ItemAttr,self).__init__()
        for field in attr.fields(self.__class__):
            is_factory = isinstance(field.default, attr.Factory)
            if is_factory and callable(field.default.factory):
                setattr(self, field.name, field.default.factory())
            else:
                setattr(self, field.name, field.default)

    
item = ItemAttr()
print(item.item_type)

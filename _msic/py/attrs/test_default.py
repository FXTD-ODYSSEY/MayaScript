import attr

@attr.s
class ItemAttr(object):
    name = property(lambda self: "{0}_0".format(self.item_type))
    
    name = attr.ib(type=str)
    item_type = attr.ib(type=str, default="asd")
    data = attr.ib(type=dict, factory=dict)
    parent = attr.ib(default=None)
    parser = attr.ib(default=None)

    @name.default
    def _(self):
        item_type = attr.fields(self.__class__).item_type.default
        return "{0}_0".format(item_type)
    
    
    
item = ItemAttr()
item.item_type = "asd"
print(item.name)

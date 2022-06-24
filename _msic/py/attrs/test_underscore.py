import attr


@attr.s
class ItemAttr(object):

    _name = attr.ib(type=str)
    


item = ItemAttr(name="asd")
print(item._name)

import attr


@attr.s
class ItemAttr(object):
    # name = property(lambda self: "{0}_0".format(self.item_type))

    name = attr.ib(type=int)
    @name.default
    def default_name(self):
        item_type = attr.fields(self.__class__).item_type.default
        return "{0}_0".format(item_type)
    item_type = attr.ib(type=str, default="asd")
    data = attr.ib(type=dict, factory=dict)
    parent = attr.ib(default=lambda: "name")
    parser = attr.ib(factory=lambda: "default_parser")

    


item = ItemAttr(name=None)
print("!!name", item.name)
item.item_type = "asd"
print(item.name)
print(item.parser)

# for field in attr.fields(item.__class__):
#     print(field.name, field.default)
#     if isinstance(field.default, attr.Factory):
#         factory = field.default.factory
#         print(factory)

# print(item.parent)

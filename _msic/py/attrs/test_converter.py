import attr


@attr.s
class ItemAttr(object):
    # name = property(lambda self: "{0}_0".format(self.item_type))

    name = attr.ib(type=int)
    @name.default
    def default_name(self):
        item_type = attr.fields(self.__class__).item_type.default
        return "{0}_0".format(item_type)

    def convert_value(value):
        print("value",value)
        return 1
    item_type = attr.ib(type=str, default="asd",converter=convert_value)

    


item = ItemAttr(name=None)
item.item_type = "2"
print(item.item_type)

# for field in attr.fields(item.__class__):
#     print(field.name, field.default)
#     if isinstance(field.default, attr.Factory):
#         factory = field.default.factory
#         print(factory)

# print(item.parent)

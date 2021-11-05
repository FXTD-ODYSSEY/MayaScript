print("import controller.mvc")

from module_test.model import carry


class TestMVC(carry.TestCarryMeta):
    pass


print(TestMVC)


class DevMVC(TestMVC):
    pass


print(DevMVC)

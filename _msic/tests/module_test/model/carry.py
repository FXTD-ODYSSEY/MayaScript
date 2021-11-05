print("import carry")
import module_test.controller.dev as dev


class TestCarry(dev.DevTest):
    pass


class TestCarryMeta(TestCarry):
    pass


def carry_all():
    print(TestCarry)


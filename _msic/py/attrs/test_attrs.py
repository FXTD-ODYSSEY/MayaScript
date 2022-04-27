import attr
from attr import validators
from addict import Dict

# from typing import data
# from six.moves import builtins


@attr.s
class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0, validator=validators.instance_of(int))
    sex = attr.ib(default="as")

    @property
    def test_property(self):
        return self.age

    def test(self):
        print("test call")


@attr.s
class TestPersoon(Person):
    work = attr.ib(default="student")



@attr.s
class Test(object):
    test_property = attr.ib(default=10)
    @property
    def test_property(self):
        return 123
# Test.test_property = Person.test_property
test = Test()
print("test_property",test.test_property)

print(isinstance(Person.test_property,property))

if __name__ == "__main__":
    first_person = TestPersoon("John", 18)
    print(first_person)
    first_person.name = "asd"
    first_person["name"] = "asd2"
    print(first_person)
    first_person.test()
    print(first_person["age"])

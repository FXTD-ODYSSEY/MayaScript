import abc
import six

class Abstract(six.with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def call(self):
        print("test")

class Base(Abstract):
    pass

# base = Base()
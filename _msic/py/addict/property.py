from addict import Addict


class Test(Addict):
    def __init__(self):
        self._data = []

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        print(value)
        self._data = value


a = Test()

a.data = 123

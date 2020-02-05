class DebugState(object):
    def __bool__(self):
        print "bool test"
        return True
    __nonzero__=__bool__

a = DebugState()
if a:
    print "test"


# class GlobalWealth(object):
#     def __init__(self):
#         self._global_wealth = 10.0
#         self._observers = []

#     @property
#     def global_wealth(self):
#         return self._global_wealth

#     @global_wealth.setter
#     def global_wealth(self, value):
#         self._global_wealth = value
#         for callback in self._observers:
#             print('announcing change')
#             callback(self._global_wealth)

#     def bind_to(self, callback):
#         print('bound')
#         self._observers.append(callback)


# class Person(object):
#     def __init__(self, data):
#         self.wealth = 1.0
#         self.data = data
#         self.data.bind_to(self.update_how_happy)
#         self.happiness = self.wealth / self.data.global_wealth

#     def update_how_happy(self, global_wealth):
#         self.happiness = self.wealth / global_wealth


# if __name__ == '__main__':
#     data = GlobalWealth()
#     p = Person(data)
#     print(p.happiness)
#     data.global_wealth = 1.0
#     print(p.happiness)
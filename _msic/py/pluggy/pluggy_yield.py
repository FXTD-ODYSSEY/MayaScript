import sys
import pluggy  # type: ignore

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    # @hookspec(firstresult=True)
    @hookspec
    def myhook(self, data):
        """My special little hook that you can customize."""


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl
    def myhook(self, data):
        for i in data:
            yield int(i) + 1


class Plugin_2:
    """A 2nd hook implementation namespace."""

    @hookimpl
    def myhook(self, data):
        for i in data:
            yield int(i) * 3


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
pm.add_hookspecs(MySpec)


def callback(result):
    print("historic call result is {result}".format(result=result))


# register plugins
pm.register(Plugin_1())
pm.register(Plugin_2())

print(pm.hook.myhook(data="123"))
for num in  pm.hook.myhook(data="123"):
    
    for i in num:
        print(i)
          
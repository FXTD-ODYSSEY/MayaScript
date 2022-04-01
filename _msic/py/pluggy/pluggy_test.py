import sys
import pluggy  # type: ignore

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    @hookspec(firstresult=True)
    def myhook(self, args):
        """My special little hook that you can customize."""
        return type("WidgetDockMixin", (), {})


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl
    def myhook(self, args):
        print("inside Plugin_1.myhook()")
        print(args)
        # return args


class Plugin_2:
    """A 2nd hook implementation namespace."""

    @hookimpl
    def myhook(self, args):
        print("inside Plugin_2.myhook()")
        print(args)


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
print(pm.hook.myhook)
pm.add_hookspecs(MySpec)


def callback(result):
    print("historic call result is {result}".format(result=result))


# register plugins
pm.register(Plugin_1())
pm.register(Plugin_2())


mixin = pm.hook.myhook(args=1)
print(mixin)
mixin_tuple = mixin if isinstance(mixin, tuple) else (mixin,)
bases = (object,)  # noqa:WPS609
mixin_tuple = tuple(set(mixin_tuple).difference(bases))
print(mixin_tuple)


import sys
import pluggy  # type: ignore

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    @hookspec(firstresult=True)
    def myhook(self, args):
        """My special little hook that you can customize."""


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl()
    def myhook(self, args):
        print("inside Plugin_1.myhook()")
        print(args)
        # msg = args[0]
        # msg = msg.upper()
        # return "msg"


class Plugin_2:
    """A 2nd hook implementation namespace."""

    @hookimpl()
    def myhook(self, args):
        print("inside Plugin_2.myhook()")
        print(args)
        return "123"


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
pm.add_hookspecs(MySpec)


def callback(result):
    print("historic call result is {result}".format(result=result))


# register plugins
pm.register(Plugin_1())
pm.register(Plugin_2())

# Add cast so that mypy knows that pm.hook
# is actually a MySpec instance. Without this
# hint there really is no way for mypy to know
# this.
res = pm.hook.myhook(args=1)
print(res)
# # this will now be caught by mypy
# HOOK = MySpec()
# module = sys.modules[__name__]
# module.HOOK = pm.hook

# def printer(msg):
#     msg = HOOK.myhook(args=(msg,))
#     print(msg)


# printer("test")

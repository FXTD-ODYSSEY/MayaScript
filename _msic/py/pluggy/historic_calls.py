import sys
from pluggy import PluginManager, HookimplMarker,HookspecMarker

hookimpl = HookimplMarker("myproject")
hookspec = HookspecMarker("myproject")

class MySpec:
    """A hook specification namespace."""

    @hookspec(historic=True)
    def myhook(self, args):
        """My special little hook that you can customize."""
        print("myhook spec")

class Plugin1:
    @hookimpl
    def myhook(self, args):
        return 1


class Plugin2:
    @hookimpl
    def myhook(self, args):
        print(1213)
        return 2

class Plugin3:
    @hookimpl
    def myhook(self, args):
        return 3

# NOTE not work for hookwrapper
# @hookimpl(hookwrapper=True)
# def myhook(args):
#     outcome = yield
#     print(outcome)

#     try:
#         outcome.get_result()
#     except RuntimeError:
#         # log the error details
#         print(outcome.excinfo)


pm = PluginManager("myproject")
pm.add_hookspecs(MySpec)
def callback(result):
    print("historic call result is {result}".format(result=result))


pm.hook.myhook.call_historic(
    kwargs={"config": 1, "args": sys.argv}, result_callback=callback
)

# register plugins
pm.register(Plugin1())
pm.register(Plugin2())
pm.register(Plugin3())

# call with history; no results returned


# # register wrapper
# pm.register(sys.modules[__name__])

# NOTE not work for direct call
# pm.hook.myhook(args=())



import sys
from pluggy import PluginManager, HookimplMarker

hookimpl = HookimplMarker("myproject")


class Plugin1:
    @hookimpl
    def myhook(self, args):
        return 1


class Plugin2:
    @hookimpl
    def myhook(self, args):
        return 2


class Plugin3:
    @hookimpl
    def myhook(self, args):
        return 3


@hookimpl(hookwrapper=True)
def myhook(args):
    outcome = yield
    print(dir(outcome))
    outcome.force_result(1)
    try:
        res = outcome.get_result()
        print(res)
    except RuntimeError:
        # log the error details
        print(outcome.excinfo)
        
    return 1


pm = PluginManager("myproject")

# register plugins
pm.register(Plugin1())
pm.register(Plugin2())
pm.register(Plugin3())

# register wrapper
pm.register(sys.modules[__name__])

# this raises RuntimeError due to Plugin2
data = pm.hook.myhook(args=())
print(data)

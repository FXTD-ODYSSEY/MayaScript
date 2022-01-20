import sys
import pluggy

hookspec = pluggy.HookspecMarker(__name__)
hookimpl = pluggy.HookimplMarker(__name__)
pm = pluggy.PluginManager(__name__)


class Spec(object):
    @hookspec()
    def call(self, b, *args):
        """call."""


pm.add_hookspecs(Spec())


@hookimpl()
def call(b, a):
    print(b,a)


pm.register(sys.modules[__name__])

HOOK = pm.hook
HOOK.call(a=5,b=2)

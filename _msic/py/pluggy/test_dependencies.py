import sys
import pluggy
from dependencies import Injector
import attr
import wrapt
hookspec = pluggy.HookspecMarker(__name__)
hookimpl = pluggy.HookimplMarker(__name__)
PM = pluggy.PluginManager(__name__)


def before(hook_name, hook_impls, kwargs):
    # print("before", hook_name, list(hook_impls), kwargs)
    # kwargs.update(impl.plugin.settings.parse_kwargs())

    kwargs["a"] = 31
    # for impl in hook_impls:
    #     print(impl)
    #     print(impl.argnames)
    #     print(impl.kwargnames)
    #     print(impl.plugin)
    #     print(impl.opts)
    return 1


def after(outcome, hook_name, hook_impls, kwargs):
    print("after", outcome, hook_name, list(hook_impls), kwargs)


undo = PM.add_hookcall_monitoring(before, after)


class Spec(object):
    @hookspec()
    def call(self, a, b):
        """call."""


PM.add_hookspecs(Spec)


@wrapt.decorator
def wrap(func,instance, args, kwargs):
    print("wrap args", args)
    return func(*args, **kwargs)


@attr.s(hash=False)
class PluginBase(object):
    settings = attr.ib()


class Plugin1(PluginBase):
    @hookimpl()
    def call(self, a, b=2, _=None):
        print(a, b)
        print(self.settings.a)
    
    def _test_call(self):
        pass

    def _inner_call(self,threshold=1):
        pass
    

@attr.s(hash=False)
class Settings:
    a = attr.ib()

@attr.s(hash=False)
class MayaService:
    a = attr.ib()


class Container(Injector):
    a = 1
    settings = Settings
    service = MayaService
    plugin1 = Plugin1


PM.register(Container.plugin1)


plug = PM.get_plugins()
print(plug)
HOOK = PM.hook
HOOK.call(a=1, b=2)

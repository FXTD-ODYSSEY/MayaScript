class Wall(object):
    STATIC_WALL_ATTR = "static wall"

    def init_wall(self):
        self.wall = "attr wall"

    def wall_info(self):
        print "this is wall of room"

    @staticmethod
    def static_wall_func():
        print 'static wall info'

class Door(object):

    def init_door(self):
        self.door = "attr door"

    def door_info(self):
        print "this is door of room"
        print self.door, self.wall, self.STATIC_WALL_ATTR
        

import inspect, sys, types

class MetaRoom(type):
    meta_members = ('Wall', "Door")
    exclude_funcs = ('__new__', '__init__')
    attr_types = (types.IntType, basestring, types.ListType, types.TupleType, types.DictType)

    def __init__(cls, name, bases, dic):
        super(metaroom, cls).__init__(name, bases, dic)　　# type.__init__(cls, name, bases, dic)
        for cls_name in metaroom.meta_members:
            cur_mod = sys.modules[__name__]
            # cur_mod = sys.modules[metaroom.__module__]
            cls_def = getattr(cur_mod, cls_name)
            for func_name, func in inspect.getmembers(cls_def, inspect.ismethod):
                # 添加成员函数
                if func_name not in metaroom.exclude_funcs:
                    assert not hasattr(cls, func_name), func_name
                    setattr(cls, func_name, func.im_func)
            for attr_name, value in inspect.getmembers(cls_def):
                # 添加静态数据成员
                if isinstance(value, metaroom.attr_types) and attr_name not in ('__module__', '__doc__'):
                    assert not hasattr(cls, attr_name), attr_name
                    setattr(cls, attr_name, value)
                    
                    
class Room(object):
    __metaclass__ = MetaRoom

    def __init__(self):
        self.room = "attr room"
        # print self.__metaclass__.meta_members
        self.add_cls_member()

    def add_cls_member(self):
        """ 分别调用各个组合类中的init_cls_name的成员函数 """
        for cls_name in self.__metaclass__.meta_members:
            init_func_name = "init_%s" % cls_name.lower()
            init_func_imp = getattr(self, init_func_name, None)
            if init_func_imp:
                init_func_imp()
                
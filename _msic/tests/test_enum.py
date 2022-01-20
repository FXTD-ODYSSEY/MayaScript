from enum import Enum
import inspect


class ItemTypes(object):
    group = "group"
    pose = "pose"
    psd = "psd"


data = ItemTypes.__slots__
print(data)

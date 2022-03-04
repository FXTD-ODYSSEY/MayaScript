import attr
from addict import Dict
from enum import auto

@attr.s
class PoseItemTypes(Dict):
    group = attr.ib(default="group")
    pose = attr.ib(default="pose")
    psd = attr.ib(default="psd")
    
PoseItemTypes = PoseItemTypes()

print(PoseItemTypes)



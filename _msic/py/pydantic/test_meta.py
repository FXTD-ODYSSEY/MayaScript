# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-06 10:32:58"


from typing import List
from typing import Any
from dataclasses import field

import json
import struct

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pydantic import Field


class Serializer(object):
    value = None
    length = 0
    c_type = ""

    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def to_bytes(self):
        return struct.pack(self.c_type, self.value)

    def from_bytes(self, bin_data, start):
        end = start + self.length
        byte_data = bin_data[start:end]
        self.value = struct.unpack(self.c_type, byte_data)
        return end

class Int2(Serializer):
    length = 2
    c_type = ">h"


class Int4(Serializer):
    length = 4
    c_type = ">i"
    
class Float(Serializer):
    length = 4
    c_type = ">f"


class String(bytes):
    @property
    def length(self):
        return Int2(len(self))


class Vector(list):
    type: Any

    @property
    def length(self):
        return Int4(len(self))


class StringMap(dict):
    @property
    def length(self):
        return Int4(len(self))

    # length = attr.ib(type=Int4)
    # key = attr.ib(type=String)
    # value = attr.ib(type=String)


class Matrix(list):
    @property
    def length(self):
        return Int4(len(self))


class BaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            Int2: lambda v: v.get(),
            Int4: lambda v: v.get(),
        }

# ----------------------------


# @attr.s
# class RawCoordinateSystem(object):
#     xAxis = attr.ib(type=Int2)
#     yAxis = attr.ib(type=Int2)
#     zAxis = attr.ib(type=Int2)


# @attr.s
# class RawLODMapping(object):
#     lods = attr.ib(default=Vector(Int2))
#     indices = attr.ib(default=Matrix(Vector(Int2)))


class Signature(bytes):
    pass


class Version(BaseModel):
    generation: Int2 = Field(default=Int2(2))
    version: Int2 = Field(default=Int2(1))

class SectionLookupTable(BaseModel):
    descriptor: Int4 = Field(default=Int4(0))
    definition: Int4 = Field(default=Int4(0))
    behavior: Int4 = Field(default=Int4(0))
    controls: Int4 = Field(default=Int4(0))
    joints: Int4 = Field(default=Int4(0))
    blend_shape_channels: Int4 = Field(default=Int4(0))
    animated_maps: Int4 = Field(default=Int4(0))
    geometry: Int4 = Field(default=Int4(0))


class RawDescriptor(BaseModel):
    marker: int
    name: String
    archetype: Int2
    gender: Int2
    age: Int2
    metadata: StringMap
    translation_unit: Int2
    rotation_unit: Int2
    # coordinate_system: RawCoordinateSystem
    lod_count: Int2
    max_lod: Int2
    complexity: String
    db_name: String


# class RawDefinition(BaseModel):
#     marker = attr.ib(type=int)
#     lod_joint_mapping = attr.ib(type=RawLODMapping)
#     lod_blend_shape_mapping = attr.ib(type=RawLODMapping)
#     lod_animated_map_mapping = attr.ib(type=RawLODMapping)
#     lod_mesh_mapping = attr.ib(type=RawLODMapping)
#     gui_control_names = attr.ib(default=Vector(String))
#     raw_control_names = attr.ib(default=Vector(String))
#     joint_names = attr.ib(default=Vector(String))
#     blend_shape_channel_names = attr.ib(default=Vector(String))
#     animated_map_names = attr.ib(default=Vector(String))
#     mesh_names = attr.ib(default=Vector(String))
#     mesh_blend_shape_channel_mapping = attr.ib()
#     joint_hierarchy = attr.ib()
#     neutral_joint_translations = attr.ib(type=RawVector3Vector)
#     neutral_joint_rotations = attr.ib(type=RawVector3Vector)


# class RawBehavior(BaseModel):
#     marker = attr.ib(type=int)
#     controls_marker = attr.ib()
#     controls = attr.ib()
#     joints_marker = attr.ib()
#     joints = attr.ib()
#     blend_shape_channels_marker = attr.ib()
#     blend_shape_channels = attr.ib()
#     animated_maps_marker = attr.ib()
#     animated_maps = attr.ib()


# class RawGeometry(BaseModel):
#     marker = attr.ib(type=int)
#     meshes = attr.ib()


class DnaBase(BaseModel):
    __slots__ = [
        "signature",
        "version",
        "sections",
        "descriptor",
        "definition",
        "behavior",
        "geometry",
        "eof",
    ]
    signature: Signature = Field(default=b"DNA")
    version: Version = Field(default_factory=Version)
    sections: SectionLookupTable = Field(default_factory=SectionLookupTable)
    # descriptor: RawDescriptor
    # definition: RawDefinition
    # behavior: RawBehavior
    # geometry: RawGeometry
    eof: Signature = Field(default=b"AND")


class Dna(DnaBase):
    def parse_dna(self, bin_data):
        pass

    def load_from_dna(self, path):
        with open(path, "rb") as rf:
            self.parse_dna(rf.read())

    def save_to_dna(self, path):
        with open(path, "wb") as wf:
            for slot in self.__slots__:
                attr_obj = getattr(self, slot)
                wf.write(attr_obj.serialize())

    def load_from_json(self, path):
        pass

    def save_to_json(self, path):
        pass

    def load(self, path):
        pass

    def save(self, path):
        pass


if __name__ == "__main__":

    dna = Dna()
    json_data = dna.json()
    print(dna.json())
    # json_str = json.dumps(json_data)
    data = Dna.parse_raw(json_data)
    print(data)

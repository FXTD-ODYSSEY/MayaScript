# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-24 14:16:57"


# Import built-in modules
import os
import json
import struct

# Import third-party modules
import attr


DIR = os.path.dirname(os.path.abspath(__file__))


@attr.s(hash=True)
class BinSerializer(object):
    value = attr.ib(default=None)
    c_fmt = ""

    @property
    def bit_length(self):
        return struct.Struct(self.c_fmt).size

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def to_bytes(self):
        return struct.pack(self.c_fmt, self.value)

    def __rrshift__(self, byte_data):
        self.value = struct.unpack(self.c_fmt, byte_data[: self.bit_length])[0]
        return byte_data[self.bit_length :]

    def __radd__(self, other):
        return other + self.to_bytes()


@attr.s(hash=True)
class Int4(BinSerializer):
    value = attr.ib(type=int, default=0)
    c_fmt = "<i"


@attr.s(hash=True)
class BinInt(BinSerializer):
    value = attr.ib(type=int, default=0)
    c_fmt = "<i"

    def to_bytes(self):
        return b"I" + struct.pack(self.c_fmt, self.value)

    def __rrshift__(self, byte_data):
        return super(BinInt, self).__rrshift__(byte_data[1:])


@attr.s(hash=True)
class BinDouble(BinSerializer):
    value = attr.ib(type=float, default=0)
    c_fmt = "d"

    def to_bytes(self):
        return b"D" + struct.pack(self.c_fmt, self.value)

    def __rrshift__(self, byte_data):
        return super(BinDouble, self).__rrshift__(byte_data[1:])


@attr.s(hash=True)
class BinString(BinSerializer):
    value = attr.ib(type=str, default="")

    def to_bytes(self):
        value = self.value if isinstance(self.value, bytes) else self.value.encode()
        return b"S" + Int4(len(value)) + value

    def __rrshift__(self, byte_data):
        size = Int4()
        offset = 1 + size.bit_length
        byte_data[1:offset] >> size
        length = size.get()
        self.value = byte_data[offset : offset + length].tobytes()
        return byte_data[offset + length :]


@attr.s(hash=True)
class BinName(BinSerializer):
    value = attr.ib(type=str, default="")
    c_fmt = "b"

    def to_bytes(self):
        return struct.pack(self.c_fmt, len(self.value)) + self.value.encode()

    def __rrshift__(self, byte_data):
        struct_fmt = struct.Struct(self.c_fmt)
        length = struct_fmt.size + struct_fmt.unpack(byte_data[: struct_fmt.size])[0]
        self.value = bytes(byte_data[struct_fmt.size : length])
        return byte_data[length:]


@attr.s(hash=True)
class BinContainerSerializer(object):
    def __rrshift__(self, byte_data):
        remainder = byte_data
        for obj in attr.fields(self.__class__):
            remainder = remainder >> getattr(self, obj.name)
        return remainder


@attr.s(hash=True)
class BinFieldBase(BinContainerSerializer):
    end_offset = attr.ib(type=Int4, default=0, converter=Int4)
    num_properties = attr.ib(type=Int4, default=1, converter=Int4)
    len_properties = attr.ib(type=Int4, default=5, converter=Int4)
    key = attr.ib(type=BinName, factory=BinName, converter=BinName)
    value = attr.ib(default=None)

    def to_bytes(self):
        return b"".join(
            [
                self.end_offset.to_bytes(),
                self.num_properties.to_bytes(),
                self.len_properties.to_bytes(),
                self.key.to_bytes(),
                self.value.to_bytes(),
            ]
        )

    def __radd__(self, other):
        self.end_offset.set(len(other + self.to_bytes()))
        return other + self.to_bytes()


@attr.s(hash=True)
class BinFieldInt(BinFieldBase):
    value = attr.ib(type=BinInt, factory=BinInt, converter=BinInt)


@attr.s(hash=True)
class BinListBase(BinSerializer):
    value = attr.ib(factory=list)
    length = attr.ib(default=0)
    value_type = None

    def to_bytes(self):
        return b"".join([val.to_bytes() for val in self.value])

    def __rrshift__(self, byte_data):
        remainder = byte_data
        for _ in range(self.length):
            obj = self.value_type()
            remainder = remainder >> obj
            self.value.append(obj)
        return remainder


@attr.s(hash=True)
class BinListString(BinListBase):
    value_type = BinString


@attr.s(hash=True)
class BinListDouble(BinListBase):
    value_type = BinDouble


@attr.s(hash=True)
class BinListVector3(BinListBase):
    value = attr.ib(factory=list)
    value_type = BinDouble

    def to_bytes(self):
        return b"".join([val.to_bytes() for val in self.value])

    def __rrshift__(self, byte_data):
        remainder = byte_data

        for _ in range(self.length):
            vector_list = []
            for _ in range(3):
                obj = self.value_type()
                remainder = remainder >> obj
                vector_list.append(obj)
            self.value.append(vector_list)

        return remainder


@attr.s(hash=True)
class InfluenceData(BinContainerSerializer):
    size = attr.ib(type=BinInt, factory=BinInt, converter=BinInt)
    models = attr.ib(type=BinListString, factory=BinListString)
    bind_pos_list = attr.ib(type=BinListVector3, factory=BinListVector3)
    weights = attr.ib(type=BinListDouble, factory=BinListDouble)

    def __rrshift__(self, byte_data):

        remainder = byte_data >> self.size

        self.models.length = self.size.get()
        remainder = remainder >> self.models
        self.bind_pos_list.length = self.size.get()
        remainder = remainder >> self.bind_pos_list
        print(self.bind_pos_list)
        self.weights.length = self.size.get()
        remainder = remainder >> self.weights
        print(self.weights)
        print("done")

        return remainder


@attr.s(hash=True)
class InfluenceDataList(BinListBase):
    value_type = InfluenceData

    def __rrshift__(self, byte_data):
        remainder = byte_data
        while remainder:
            obj = self.value_type()
            remainder = remainder >> obj
            self.value.append(obj)


@attr.s(hash=True)
class BinFieldInfluenceDataList(BinFieldBase):
    value = attr.ib(factory=InfluenceDataList)

    def __rrshift__(self, byte_data):

        remainder = byte_data
        for obj in attr.fields(self.__class__)[:-1]:
            remainder = remainder >> getattr(self, obj.name)

        start = len(byte_data.obj) - len(remainder)
        end = self.end_offset.get() - start
        remainder[:end] >> self.value

        return remainder[end:]


@attr.s(hash=True)
class BinBlindData(BinContainerSerializer):
    version = attr.ib(type=BinFieldInt, factory=BinFieldInt, converter=BinFieldInt)
    marker_count = attr.ib(type=BinFieldInt, factory=BinFieldInt, converter=BinFieldInt)
    influence_data = attr.ib(
        type=BinFieldInfluenceDataList,
        factory=BinFieldInfluenceDataList,
        converter=BinFieldInfluenceDataList,
    )


class BinJSonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        return super(BinJSonEncoder, self).default(self, obj)

    @staticmethod
    def serialize(inst, field, value):
        if isinstance(value, BinSerializer):
            return value.value
        return value


def main():
    with open(os.path.join(DIR, "raw_1"), "rb") as rf:
        bin_data = memoryview(rf.read())

    blind_data = BinBlindData()
    bin_data[1:] >> blind_data
    print(blind_data)

    data = attr.asdict(blind_data, value_serializer=BinJSonEncoder.serialize)
    with open(os.path.join(DIR,"bin2json.json"), "w") as wf:
        json.dump(data,wf, cls=BinJSonEncoder)

    # a = Int4()
    # b = Int4()
    # bin_data = b"\x03\x00\x00\x00\x32\x00\x00\x00"
    # mem = memoryview(bin_data)
    # for obj in [a, b]:
    #     mem = mem >> obj
    # print(a)
    # print(b)


if __name__ == "__main__":
    main()


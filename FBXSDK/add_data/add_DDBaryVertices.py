# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-20 15:53:30"

# Import built-in modules
from collections import defaultdict
from collections import namedtuple
from functools import partial
import json
import os
import struct
import attr

# Import third-party modules
import FbxCommon
from fbx import FbxActionDT
from fbx import FbxBlobDT
from fbx import FbxBoolDT
from fbx import FbxCharPtrDT
from fbx import FbxDouble3
from fbx import FbxDouble3DT
from fbx import FbxDoubleDT
from fbx import FbxEnumDT
from fbx import FbxIntDT
from fbx import FbxBlob
from fbx import FbxMesh
from fbx import FbxNode
from fbx import FbxProperty
from fbx import FbxString
from fbx import FbxStringDT

DIR = os.path.dirname(__file__)

Triangle = namedtuple("Triangle", ["A", "B", "C"])
ZERO_TRI = Triangle(0, 0, 0)
NUM_BARY_VERTEX = 32


@attr.s(hash=True)
class BinSerializer(object):
    value = attr.ib()
    c_fmt = ""

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def to_bytes(self):
        return struct.pack(self.c_fmt, self.value)

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


@attr.s(hash=True)
class BinDouble(BinSerializer):
    value = attr.ib(type=float, default=0)
    c_fmt = "d"

    def to_bytes(self):
        return b"D" + struct.pack(self.c_fmt, self.value)


@attr.s(hash=True)
class BinName(BinSerializer):
    value = attr.ib(type=str, default="")
    c_fmt = "b"

    def to_bytes(self):
        return struct.pack(self.c_fmt, len(self.value)) + self.value.encode()


@attr.s(hash=True)
class BinString(BinSerializer):
    value = attr.ib(type=str, default="")

    def to_bytes(self):
        value = self.value if isinstance(self.value, bytes) else self.value.encode()
        return b"S" + Int4(len(value)) + value

    
@attr.s(hash=True)
class BinField(BinSerializer):
    key = attr.ib(type=BinName, factory=BinName, converter=BinName)
    value = attr.ib(type=BinInt, factory=BinInt, converter=BinInt)
    end_offset = attr.ib(type=Int4, default=0, converter=Int4)
    num_properties = attr.ib(type=Int4, default=1, converter=Int4)
    len_properties = attr.ib(type=Int4, default=5, converter=Int4)

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
class BinFieldInt(BinField):
    pass

def build_tri_list(mesh):
    tri_list = []
    poly_verts = mesh.GetPolygonVertices()
    for poly_index in range(mesh.GetPolygonCount()):
        start_index = mesh.GetPolygonVertexIndex(poly_index)
        vert_a = poly_verts[start_index]
        for size_index in range(1, mesh.GetPolygonSize(poly_index) - 1):
            vert_b = poly_verts[start_index + size_index]
            vert_c = poly_verts[start_index + size_index + 1]
            tri_list.append(Triangle(vert_a, vert_b, vert_c))
    return tri_list


def build_skin_data(mesh):
    skin_data = {}
    skin = mesh.GetDeformer(0)
    for cluster_index in range(skin.GetClusterCount()):
        cluster = skin.GetCluster(cluster_index)
        src_object = cluster.GetSrcObject()
        skin_data[src_object.GetName()] = {
            index: weight
            for index, weight in zip(
                cluster.GetControlPointIndices(), cluster.GetControlPointWeights()
            )
        }
    return skin_data


def create_property(root_prop, name, value_type, value=None):
    prop = FbxProperty.Create(root_prop, value_type, name)
    if value is not None:
        prop.Set(value)
    return prop

def transform(vector, matrix):
    x = sum([vector[i] * matrix[i][0] for i in range(4)])
    y = sum([vector[i] * matrix[i][1] for i in range(4)])
    z = sum([vector[i] * matrix[i][2] for i in range(4)])
    return (x, y, z)


def main(fbx_path, json_path):
    # NOTES(timmyliang): validate path
    assert os.path.exists(fbx_path)
    assert os.path.exists(json_path)

    # NOTES(timmyliang): load json
    with open(json_path, "r") as rf:
        marker_data = json.load(rf)

    # NOTES(timmyliang): load fbx
    manager, scene = FbxCommon.InitializeSdkObjects()
    assert FbxCommon.LoadScene(manager, scene, fbx_path)

    for i in range(scene.GetNodeCount()):
        node = scene.GetNode(i)
        if node.GetName() != "M_shoes_geo":
            continue

        mesh = node.GetMesh()
        tri_list = build_tri_list(mesh)
        skin_data = build_skin_data(mesh)

        # NOTES(timmyliang): add mesh
        bary_node = FbxNode.Create(manager, "DDBaryVertices")
        bary_mesh = FbxMesh.Create(manager, "DDBaryVertices_mesh")
        bary_node.SetNodeAttribute(bary_mesh)
        node.AddChild(bary_node)

        add_property = partial(create_property, bary_node.RootProperty)

        # NOTES(timmyliang): add property
        # prop = bary_node.RootProperty.Find("ScalingMax")
        # prop.IsValid() and prop.Destroy()
        # TODO(timmyliang): ScalingMin not work
        # bary_node.ScalingMaxX.Set(False)
        # bary_node.ScalingMaxY.Set(False)
        # bary_node.ScalingMaxZ.Set(False)
        bary_node.ScalingMinX.Set(True)
        bary_node.ScalingMinY.Set(True)
        bary_node.ScalingMinZ.Set(True)
        bary_node.ScalingMin.Set(FbxDouble3(1.0, 1.0, 1.0))
        add_property("DefaultAttributeIndex", FbxIntDT)
        add_property("MoBuSubTypeName", FbxCharPtrDT, FbxString("BaryVertexModel"))
        add_property(
            "MoBuObjectFullName", FbxCharPtrDT, FbxString("Model::DDBaryVertices")
        )
        add_property("MultiTake", FbxIntDT, 1)
        add_property("DefaultKeyingGroup", FbxIntDT)
        add_property("DefaultKeyingGroupEnum", FbxEnumDT)
        add_property("ManipulationMode", FbxEnumDT)
        add_property("ScalingPivotUpdateOffset", FbxDouble3DT)
        add_property("SetPreferedAngle", FbxActionDT)
        add_property("PivotsVisibility", FbxEnumDT, 1)
        add_property("RotationLimitsVisibility", FbxBoolDT)
        add_property("LocalTranslationRefVisibility", FbxBoolDT)
        add_property("RotationRefVisibility", FbxBoolDT)
        add_property("RotationAxisVisibility", FbxBoolDT)
        add_property("ScalingRefVisibility", FbxBoolDT)
        add_property("HierarchicalCenterVisibility", FbxBoolDT)
        add_property("GeometricCenterVisibility", FbxBoolDT)
        add_property("ReferentialSize", FbxDoubleDT, 12)
        add_property("Pickable", FbxBoolDT, True)
        add_property("Transformable", FbxBoolDT, True)
        add_property("CullingMode", FbxEnumDT)
        add_property("ShowTrajectories", FbxBoolDT)
        add_property("MoBuRelationBlindData", FbxStringDT)

        # NOTES(timmyliang): add marker property
        add_property("Is Live", FbxBoolDT, True)
        add_property("Is Source", FbxBoolDT, True)
        marker_itr = iter(marker_data)
        influence_data = defaultdict(lambda: defaultdict(list))
        for index in range(NUM_BARY_VERTEX):
            itr = iter(next(marker_itr, []))
            tri_index = next(itr, None)
            u_value = next(itr, 0)
            v_value = next(itr, 0)
            is_enable = bool(tri_index)

            tri = tri_list[tri_index] if is_enable else ZERO_TRI
            add_property("MarkerA {0}".format(index), FbxIntDT, tri.A)
            add_property("MarkerB {0}".format(index), FbxIntDT, tri.B)
            add_property("MarkerC {0}".format(index), FbxIntDT, tri.C)
            add_property("U {0}".format(index), FbxDoubleDT, u_value)
            add_property("V {0}".format(index), FbxDoubleDT, v_value)
            add_property("Enabled {0}".format(index), FbxBoolDT, is_enable)
            if is_enable:
                for joint, vert_weight in skin_data.items():
                    for vert_index in [tri.A, tri.B, tri.C]:
                        if vert_index not in vert_weight:
                            continue

                        influence_data[vert_index]["joints"].append(joint)

                        pos = mesh.GetControlPointAt(vert_index)
                        matrix = node.EvaluateGlobalTransform()
                        bind_pos = transform(pos, matrix.Inverse())
                        influence_data[vert_index]["bind_pos_list"].append(bind_pos)

                        weight = vert_weight[vert_index]
                        influence_data[vert_index]["weights"].append(weight)

        # NOTES(timmyliang): convert dump_data to fbx binary format
        bin_data = b"\x70"
        bin_data += BinFieldInt("BaryVertexVersion", 1)
        bin_data += BinFieldInt("BaryVertexMarkerCount", len(marker_data))
        # NOTES(timmyliang): write BaryVertexInfluenceData end_offset ...
        bin_data += b"\x74\x0D\x00\x00\x38\x01\x00\x00\x05\x0D\x00\x00"
        bin_data += BinName("BaryVertexInfluenceData")

        # TODO(timmyliang): order?
        for vert_index, data in influence_data.items():
            joints = data["joints"]
            bin_data += BinInt(len(joints))
            for joint in joints:
                bin_data += BinString(joint.encode() + struct.pack(">h", 1) + b"Model")

            for bind_pos in data["bind_pos_list"]:
                for axis_value in bind_pos:
                    bin_data += BinDouble(axis_value)

            for weight in data["weights"]:
                bin_data += BinDouble(weight)

        bin_data += b"\x00" * 13
        print(len(bin_data))
        # print(json.dumps(influence_data))
        # TODO(timmyliang): write data 
        print(bin_data[33:55])
        blob = FbxBlob(len(bin_data))
        blob.Assign(bin_data,len(bin_data))
        add_property("MoBuAttrBlindData", FbxBlobDT, FbxString(blob))


    with open(os.path.join(DIR, "raw_py"), "wb") as wf:
        wf.write(bin_data)

    output_path = os.path.join(DIR, "test.fbx")
    FbxCommon.SaveScene(manager, scene, output_path)


if __name__ == "__main__":
    fbx_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Assets\Actor\Daodao02\DaodaoFlat\Rigging\Live_Rig\Rig\Actor_Daodao02_DaodaoFlat_Mocap_Rig_ascii_fix.fbx"
    json_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Live\Config\Templates\ShoesContact\Shoes_XueyiFlat.txt"
    main(fbx_path, json_path)

# -*- coding: utf-8 -*-
"""
Add BaryVertexModel custom mesh with FBXSDK.
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
from collections import defaultdict
from collections import namedtuple
from functools import partial
import json
import os
import struct

# Import third-party modules
import FbxCommon
import attr
from fbx import FbxActionDT
from fbx import FbxBlobDT
from fbx import FbxBoolDT
from fbx import FbxCharPtrDT
from fbx import FbxDouble3
from fbx import FbxDouble3DT
from fbx import FbxDoubleDT
from fbx import FbxEnumDT
from fbx import FbxIntDT
from fbx import FbxMesh
from fbx import FbxNode
from fbx import FbxProperty
from fbx import FbxString
from fbx import FbxStringDT

DIR = os.path.dirname(__file__)

Triangle = namedtuple("Triangle", ["A", "B", "C"])
ZERO_TRI = Triangle(0, 0, 0)
NUM_BARY_VERTEX = 32


@attr.s
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


@attr.s
class Int4(BinSerializer):
    value = attr.ib(type=int, default=0)
    c_fmt = "<i"


@attr.s
class BinInt(BinSerializer):
    """FBX Int Type.
    https://code.blender.org/2013/08/fbx-binary-file-format-specification/#property-record-format
    """

    value = attr.ib(type=int, default=0)
    c_fmt = "<i"

    def to_bytes(self):
        return b"I" + struct.pack(self.c_fmt, self.value)


@attr.s
class BinDouble(BinSerializer):
    """FBX Double Type.
    https://code.blender.org/2013/08/fbx-binary-file-format-specification/#property-record-format
    """

    value = attr.ib(type=float, default=0.0)
    c_fmt = "d"

    def to_bytes(self):
        return b"D" + struct.pack(self.c_fmt, self.value)


@attr.s
class BinString(BinSerializer):
    """FBX String Type.
    https://code.blender.org/2013/08/fbx-binary-file-format-specification/#property-record-format
    """

    value = attr.ib(type=str, default="")

    def to_bytes(self):
        value = self.value if isinstance(self.value, bytes) else self.value.encode()
        return b"S" + Int4(len(value)) + value


@attr.s
class BinName(BinSerializer):
    value = attr.ib(type=str, default="")
    c_fmt = "b"

    def to_bytes(self):
        return struct.pack(self.c_fmt, len(self.value)) + self.value.encode()


@attr.s
class BinFieldBase(BinSerializer):
    """FBX Field Node.
    https://code.blender.org/2013/08/fbx-binary-file-format-specification/#node-record-format
    Need to provide `end_offset` `num_properties` `len_properties` for serialize.
    """

    end_offset = attr.ib(type=Int4, default=0, converter=Int4)
    num_properties = attr.ib(type=Int4, default=0, converter=Int4)
    len_properties = attr.ib(type=Int4, default=0, converter=Int4)
    key = attr.ib(type=BinName, factory=BinName, converter=BinName)
    value = attr.ib(default=None)

    def to_bytes(self):
        bin_data = b""
        for filed in attr.fields(self.__class__):
            bin_data += getattr(self, filed.name)
        return bin_data

    def __radd__(self, other):
        self.end_offset.set(len(other + self.to_bytes()))
        return other + self.to_bytes()


@attr.s
class BinFieldInt(BinFieldBase):
    num_properties = attr.ib(type=Int4, default=1, converter=Int4)
    len_properties = attr.ib(type=Int4, default=5, converter=Int4)
    value = attr.ib(type=BinInt, factory=BinInt, converter=BinInt)


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


def create_property(root_prop, name, value_type, value=None):
    prop = FbxProperty.Create(root_prop, value_type, name)
    if value is not None:
        prop.Set(value)
    return prop


def transform(vector, matrix):
    return [
        sum([vector[i] * matrix[i][index] for i in range(3)]) + matrix[3][index]
        for index in range(3)
    ]


def add_bary_vertex_model(fbx_path, json_path, output_path, node_name="M_shoes_geo"):
    """Add MotionBuilder BaryVertex Model to mesh.

    Args:
        fbx_path (_type_): _description_
        json_path (_type_): _description_
        output_path (_type_): _description_
        node_name (str, optional): _description_. Defaults to "M_shoes_geo".
    """
    # NOTES(timmyliang): validate path
    assert os.path.exists(fbx_path)
    assert os.path.exists(json_path)

    # NOTES(timmyliang): load fbx
    manager, scene = FbxCommon.InitializeSdkObjects()
    assert FbxCommon.LoadScene(manager, scene, fbx_path)

    # NOTES(timmyliang): load json
    with open(json_path, "r") as rf:
        marker_data = json.load(rf)

    node = scene.FindNodeByName(node_name)
    assert node, "{0} not found".format(node_name)

    mesh = node.GetMesh()
    tri_list = build_tri_list(mesh)

    # NOTES(timmyliang): add mesh
    bary_node = FbxNode.Create(manager, "DDBaryVertices")
    bary_mesh = FbxMesh.Create(manager, "DDBaryVertices_mesh")
    bary_node.SetNodeAttribute(bary_mesh)
    node.AddChild(bary_node)

    add_property = partial(create_property, bary_node.RootProperty)

    # NOTES(timmyliang): add property
    # TODO(timmyliang): ScalingMin not work
    prop = bary_node.RootProperty.Find("ScalingMax")
    prop.IsValid() and prop.Destroy()
    add_property("ScalingMin", FbxDouble3DT, FbxDouble3(1.0, 1.0, 1.0))
    add_property("DefaultAttributeIndex", FbxIntDT)
    add_property("MoBuSubTypeName", FbxCharPtrDT, FbxString("BaryVertexModel"))
    add_property("MoBuObjectFullName", FbxCharPtrDT, FbxString("Model::DDBaryVertices"))
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

    marker_itr = iter(marker_data)
    influence_data = defaultdict(lambda: defaultdict(list))
    skin = mesh.GetDeformer(0)
    for index in range(NUM_BARY_VERTEX):
        itr = iter(next(marker_itr, []))
        tri_index = next(itr, None)
        u_value = next(itr, 0)
        v_value = next(itr, 0)
        is_enable = bool(tri_index)

        tri = tri_list[tri_index] if is_enable else ZERO_TRI
        # NOTES(timmyliang): add marker property
        add_property("MarkerA {0}".format(index), FbxIntDT, tri.A)
        add_property("MarkerB {0}".format(index), FbxIntDT, tri.B)
        add_property("MarkerC {0}".format(index), FbxIntDT, tri.C)
        add_property("U {0}".format(index), FbxDoubleDT, u_value)
        add_property("V {0}".format(index), FbxDoubleDT, v_value)
        add_property("Enabled {0}".format(index), FbxBoolDT, is_enable)
        if is_enable:
            # NOTES(timmyliang): collect influence_data for bin data
            for cluster_index in range(skin.GetClusterCount()):
                cluster = skin.GetCluster(cluster_index)
                verts = cluster.GetControlPointIndices()
                for pt_index, vert_index in enumerate(verts):
                    pos = mesh.GetControlPointAt(vert_index)
                    for tri_index, tri_vert in enumerate([tri.A, tri.B, tri.C]):
                        if tri_vert == vert_index:
                            idx = index * 3 + tri_index
                            joint = cluster.GetSrcObject()
                            influence_data[idx]["joints"].append(joint.GetName())

                            matrix = joint.EvaluateGlobalTransform()
                            bind_pos = transform(pos, matrix.Inverse())
                            influence_data[idx]["bind_pos_list"].append(bind_pos)

                            weight = cluster.GetControlPointWeights()[pt_index]
                            influence_data[idx]["weights"].append(weight)

    add_property("Is Live", FbxBoolDT, True)
    add_property("Is Source", FbxBoolDT, True)

    bin_data = b"\x70"
    bin_data += BinFieldInt(key="BaryVertexVersion", value=1)
    bin_data += BinFieldInt(key="BaryVertexMarkerCount", value=len(marker_data))

    bin_influence_field = b""
    bin_influence_field += BinName("BaryVertexInfluenceData")
    property_offset = len(bin_influence_field)

    # NOTES(timmyliang): convert influence_data to fbx binary format
    num_properties = 0
    for vert_index, data in sorted(influence_data.items()):
        joints = data["joints"]
        num_properties += 1
        bin_influence_field += BinInt(len(joints))
        for joint in joints:
            num_properties += 1
            joint_name = joint.encode() + struct.pack(">h", 1) + b"Model"
            bin_influence_field += BinString(joint_name)

        for bind_pos in data["bind_pos_list"]:
            for axis_value in bind_pos:
                num_properties += 1
                bin_influence_field += BinDouble(axis_value)

        for weight in data["weights"]:
            num_properties += 1
            bin_influence_field += BinDouble(weight)

    # NOTES(timmyliang): 12 is Int4 * 3
    end_offset = len(bin_data) + 12 + len(bin_influence_field)
    len_properties = len(bin_influence_field) - property_offset
    
    # NOTES(timmyliang): https://code.blender.org/2013/08/fbx-binary-file-format-specification/#node-record-format
    bin_data += Int4(end_offset)
    bin_data += Int4(num_properties)
    bin_data += Int4(len_properties)
    bin_data += bin_influence_field
    bin_data += b"\x00" * 13

    BLOB_STUB = b"*" * len(bin_data)
    # NOTES(timmyliang): FBXSDK not support write blob data so I add a stub data for replacement
    add_property("MoBuAttrBlindData", FbxBlobDT, FbxString(BLOB_STUB))

    FbxCommon.SaveScene(manager, scene, output_path, 0)

    # NOTES(timmyliang): write blob data
    with open(output_path, "rb+") as rf:
        content = rf.read()
        rf.seek(0)
        rf.write(content.replace(BLOB_STUB, bin_data))


if __name__ == "__main__":
    fbx_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Assets\Actor\Daodao02\DaodaoFlat\Rigging\Live_Rig\Rig\Actor_Daodao02_DaodaoFlat_Mocap_Rig.fbx"
    json_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Live\Config\Templates\ShoesContact\Shoes_XueyiFlat.txt"
    output_path = os.path.join(DIR, "test.fbx")
    add_bary_vertex_model(fbx_path, json_path, output_path)


# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-04-10 11:00:01"

import os
import json
import struct
from textwrap import dedent
from functools import partial
from collections import defaultdict, OrderedDict

import renderdoc as rd
import qrenderdoc


class MeshData(rd.MeshFormat):
    indexOffset = 0
    name = ""


def unpackData(fmt, data):
    # We don't handle 'special' formats - typically bit-packed such as 10:10:10:2
    if fmt.Special():
        raise RuntimeError("Packed formats are not supported!")

    formatChars = {}
    #                                 012345678
    formatChars[rd.CompType.UInt] = "xBHxIxxxL"
    formatChars[rd.CompType.SInt] = "xbhxixxxl"
    formatChars[rd.CompType.Float] = "xxexfxxxd"  # only 2, 4 and 8 are valid

    # These types have identical decodes, but we might post-process them
    formatChars[rd.CompType.UNorm] = formatChars[rd.CompType.UInt]
    formatChars[rd.CompType.UScaled] = formatChars[rd.CompType.UInt]
    formatChars[rd.CompType.SNorm] = formatChars[rd.CompType.SInt]
    formatChars[rd.CompType.SScaled] = formatChars[rd.CompType.SInt]

    # We need to fetch compCount components
    vertexFormat = str(fmt.compCount) + formatChars[fmt.compType][fmt.compByteWidth]

    # Unpack the data
    value = struct.unpack_from(vertexFormat, data, 0)

    # If the format needs post-processing such as normalisation, do that now
    if fmt.compType == rd.CompType.UNorm:
        divisor = float((2 ** (fmt.compByteWidth * 8)) - 1)
        value = tuple(float(i) / divisor for i in value)
    elif fmt.compType == rd.CompType.SNorm:
        maxNeg = -float(2 ** (fmt.compByteWidth * 8)) / 2
        divisor = float(-(maxNeg - 1))
        value = tuple(
            (float(i) if (i == maxNeg) else (float(i) / divisor)) for i in value
        )

    # If the format is BGRA, swap the two components
    if fmt.BGRAOrder():
        value = tuple(value[i] for i in [2, 1, 0, 3])

    return value


def getIndices(controller, mesh):
    # Get the character for the width of index
    indexFormat = "B"
    if mesh.indexByteStride == 2:
        indexFormat = "H"
    elif mesh.indexByteStride == 4:
        indexFormat = "I"

    # Duplicate the format by the number of indices
    indexFormat = str(mesh.numIndices) + indexFormat

    # If we have an index buffer
    if mesh.indexResourceId != rd.ResourceId.Null():
        # Fetch the data
        ibdata = controller.GetBufferData(mesh.indexResourceId, mesh.indexByteOffset, 0)

        # Unpack all the indices, starting from the first index to fetch
        offset = mesh.indexOffset * mesh.indexByteStride
        indices = struct.unpack_from(indexFormat, ibdata, offset)

        # Apply the baseVertex offset
        return [i + mesh.baseVertex for i in indices]
    else:
        # With no index buffer, just generate a range
        return tuple(range(mesh.numIndices))


def findChannel(vertexData, keywords):
    for channel in vertexData:
        for keyword in keywords:
            if keyword in channel:
                return channel
    return None


def unpack(controller, attr, idx):
    # This is the data we're reading from. This would be good to cache instead of
    # re-fetching for every attribute for every index
    offset = attr.vertexByteOffset + attr.vertexByteStride * idx
    data = controller.GetBufferData(attr.vertexResourceId, offset, 0)

    # Get the value from the data
    return unpackData(attr.format, data)


def get_data(meshInputs, controller):

    indices = getIndices(controller, meshInputs[0])
    if not indices:
        # manager.ErrorDialog("Current Draw Call lack of Vertex. ", "Error")
        return

    # We'll decode the first three indices making up a triangle
    idx_dict = defaultdict(list)
    value_dict = defaultdict(list)
    vertex_data = defaultdict(OrderedDict)
    for i, idx in enumerate(indices):
        for attr in meshInputs:
            value = unpack(controller, attr, idx)
            idx_dict[attr.name].append(idx)
            value_dict[attr.name].append(value)
            if idx not in vertex_data[attr.name]:
                vertex_data[attr.name][idx] = value

    print(len(value_dict))


def main():

    state = pyrenderdoc.CurPipelineState()

    # Get the index & vertex buffers, and fixed vertex inputs
    ib = state.GetIBuffer()
    vbs = state.GetVBuffers()
    attrs = state.GetVertexInputs()

    # NOTE current draw draw
    draw = pyrenderdoc.CurSelectedDrawcall()
    if not draw:
        msg = "Please pick a valid draw call in the Event Browser."
        manager.ErrorDialog(msg, "Error")
        return

    meshInputs = []
    for attr in attrs:
        if not attr.used:
            continue
        elif attr.perInstance:
            # We don't handle instance attributes
            manager.ErrorDialog("Instanced properties are not supported!", "Error")
            return

        meshInput = MeshData()
        meshInput.indexResourceId = ib.resourceId
        meshInput.indexByteOffset = ib.byteOffset
        meshInput.indexByteStride = draw.indexByteWidth
        meshInput.baseVertex = draw.baseVertex
        meshInput.indexOffset = draw.indexOffset
        meshInput.numIndices = draw.numIndices

        # If the draw doesn't use an index buffer, don't use it even if bound
        if not (draw.flags & rd.DrawFlags.Indexed):
            meshInput.indexResourceId = rd.ResourceId.Null()

        # The total offset is the attribute offset from the base of the vertex
        meshInput.vertexByteOffset = (
            attr.byteOffset
            + vbs[attr.vertexBuffer].byteOffset
            + draw.vertexOffset * vbs[attr.vertexBuffer].byteStride
        )
        meshInput.format = attr.format
        meshInput.vertexResourceId = vbs[attr.vertexBuffer].resourceId
        meshInput.vertexByteStride = vbs[attr.vertexBuffer].byteStride
        meshInput.name = attr.name

        meshInputs.append(meshInput)

    pyrenderdoc.Replay().BlockInvoke(partial(get_data, meshInputs))


if __name__ == "__main__":
    main()

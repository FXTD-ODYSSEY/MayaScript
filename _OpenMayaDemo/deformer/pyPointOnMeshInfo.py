#
# ==========================================================================
# Copyright 2015 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk
# license agreement provided at the time of installation or download,
# or which otherwise accompanies this software in either electronic
# or hard copy form.
# ==========================================================================
#

import sys
import maya.api.OpenMaya as om

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass

# FUNCTION THAT FINDS THE POINT AND NORMAL OF A POLY AT A SPECIFIED FACE UV COORD ABOUT A SPECIFIED FACE:
def getPointAndNormal(meshDagPath, faceIndex, relative, parameterU, parameterV, point, normal, theMesh):
	polyObj = meshDagPath
	if not theMesh.isNull():
		polyObj = theMesh
	# CREATE FACE ITERATOR, AND SET ITS INDEX TO THAT OF THE SPECIFIED FACE:
	faceIter = om.MItMeshPolygon(polyObj)
	faceIter.setIndex(faceIndex)

	# WHEN "RELATIVE" MODE IS SPECIFIED, CALCULATE THE *ABSOLUTE* UV'S FROM THE SPECIFIED FACE AND "RELATIVE" UV'S:
	# OTHERWISE, JUST TAKE THE ABSOLUTE UV'S TO BE THE ONES SPECIFIED:
	u = parameterU
	v = parameterV
	if relative:
		uvs = faceIter.getUVs()
		uArray = uvs[0]
		vArray = uvs[1]
		minU=999999
		minV=999999
		maxU=0
		maxV=0
		for i in range(len(uArray)):
			if uArray[i] < minU:
				minU = uArray[i]
			if vArray[i] < minV:
				minV = vArray[i]
			if uArray[i] > maxU:
				maxU = uArray[i]
			if vArray[i] > maxV:
				maxV = vArray[i]

		u = minU + parameterU * (maxU - minU)
		v = minV + parameterV * (maxV - minV)

	# FIND THE WORLDSPACE COORDINATE AT THE SPECIFIED UV:
	UV = [u, v]
	try:
		newPoint = faceIter.getPointAtUV(UV, om.MSpace.kWorld)
		point.x = newPoint.x
		point.y = newPoint.y
		point.z = newPoint.z
		point.w = newPoint.w
	except:
		pass

	# FIND THE NORMAL AT THE SPECIFIED UV:
	meshFn = om.MFnMesh(meshDagPath)
	if not theMesh.isNull():
		meshFn.setObject(theMesh)
	newNormal = meshFn.getClosestNormal(point, om.MSpace.kWorld)
	normal.x = newNormal[0].x
	normal.y = newNormal[0].y
	normal.z = newNormal[0].z

#
# MAIN CLASS DECLARATION FOR THE MEL COMMAND:
#
class pointOnMeshCommand(om.MPxCommand):
	nodeCreated = False
	positionSpecified = False
	normalSpecified = False
	faceIndexSpecified = False
	relativeSpecified = False
	parameterUSpecified = False
	parameterVSpecified = False
	meshNodeName = ""
	pointOnMeshInfoName = ""
	faceIndex = -1
	relative = False
	parameterU = 0.0
	parameterV = 0.0

	def __init__(self):
		om.MPxCommand.__init__(self)

	# METHOD FOR CREATING AN INSTANCE OF THIS COMMAND:
	@staticmethod
	def cmdCreator():
		return pointOnMeshCommand()
		
	# MAKE THIS COMMAND UNDOABLE:
	def isUndoable(self):
		return True

	# FIRST INVOKED WHEN COMMAND IS CALLED, PARSING THE COMMAND ARGUMENTS, INITIALIZING DEFAULT PARAMETERS, THEN CALLING redoIt():
	def doIt(self, args):
		# PARSE THE COMMAND'S ARGUMENTS:
		for i in range(len(args)):
			if ("-name" == args.asString(i)) or ("-na" == args.asString(i)):
				i = i+1
				self.pointOnMeshInfoName = args.asString(i)

			elif ("-position" == args.asString(i)) or ("-p" == args.asString(i)):
				self.positionSpecified = True

			elif ("-normal" == args.asString(i)) or ("-nr" == args.asString(i)):
				self.normalSpecified = True

			elif ("-faceIndex" == args.asString(i)) or ("-f" == args.asString(i)):
				self.faceIndexSpecified = True
				i = i+1
				temp = args.asInt(i)
				if temp < 0:
					raise ValueError("Invalid faceIndex!")
				faceIndex = temp

			elif ("-relative" == args.asString(i)) or ("-r" ==args.asString(i)):
				self.relativeSpecified = True
				i = i+1
				self.relative = args.asBool(i)

			elif ("-parameterU" == args.asString(i)) or ("-u" == args.asString(i)):
				self.parameterUSpecified = True
				i = i+1
				temp = args.asDouble(i)
				if temp < 0 or temp > 1:
					raise ValueError("Invalid parameterU!")
				self.parameterU = temp

			elif ("-parameterV" == args.asString(i)) or ("-v" == args.asString(i)):
				self.parameterVSpecified = True
				i = i+1
				temp = args.asDouble(i)
				if temp < 0 or temp > 1:
					raise ValueError("Invalid parameterV!")
				self.parameterV = temp

			elif i == (len(args)-1):
				self.meshNodeName = args.asString(i)

			else:
				raise ValueError("Invalid flag:" + args.asString(i))

		# MAKE SURE UNSPECIFIED INPUT PARAMETER FLAGS GET DEFAULT VALUES:
		if not self.faceIndexSpecified:
			self.faceIndex = 0
		if not self.relativeSpecified:
			self.relative = True
		if not self.parameterUSpecified:
			parameterU = 0.5
		if not self.parameterVSpecified:
			self.parameterV = 0.5

		# DO THE WORK:
		self.redoIt()

	# DOES MOST OF THE WORK IN COMPUTING THE POSITION, NORMAL, OR CREATING A "pointOnMeshInfo" NODE:
	def redoIt(self):
		# WHEN NO MESH IS SPECIFIED IN THE COMMAND, GET THE FIRST SELECTED MESH FROM THE SELECTION LIST:
		sList = om.MSelectionList()
		if self.meshNodeName == "":
			sList = om.MGlobal.getActiveSelectionList()
			if sList.length() == 0:
				raise ValueError("No mesh or mesh transform specified!")

		# OTHERWISE, USE THE NODE NAME SPECIFIED IN THE LAST ARGUMENT OF THE COMMAND:
		else:
			sList.add(self.meshNodeName)

		# RETRIEVE THE FIRST ITEM FROM THE SELECTION LIST:
		meshDagPath = sList.getDagPath(0)

		# CREATE AND CONNECT A "pointOnMeshInfo" NODE, OR GET THE POINT AND NORMAL ACCORDING TO
		# WHETHER THE "-position/-p" AND/OR "-normal/-nr" FLAGS WERE SPECIFIED, AND WHETHER THE MESH
		# "SHAPE" OR ITS "TRANSFORM" WAS SPECIFIED/SELECTED:
		point = om.MPoint()
		normal = om.MVector()
		# WHEN THE SPECIFIED NODE IS THE MESH "SHAPE":
		if meshDagPath.node().hasFn(om.MFn.kMesh):
			# WHEN NEITHER "-position/-p" NOR "-normal/-nr" ARE SPECIFIED, CREATE AND CONNECT A "pointOnMeshInfo" NODE AND RETURN ITS NODE NAME:
			if not self.positionSpecified and not self.normalSpecified:
				# CREATE THE NODE:
				self.nodeCreated = True
				depNodeFn = om.MFnDependencyNode()

				if self.pointOnMeshInfoName == "":
					depNodeFn.create("pointOnMeshInfo")
				else:
					depNodeFn.create("pointOnMeshInfo", self.pointOnMeshInfoName)
				self.pointOnMeshInfoName = depNodeFn.name()

				# SET THE ".faceIndex" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.faceIndexSpecified:
					faceIndexPlug = depNodeFn.findPlug("faceIndex", True)
					faceIndexPlug.setValue(self.faceIndex)

				# SET THE ".relative" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.relativeSpecified:
					relativePlug = depNodeFn.findPlug("relative", True)
					relativePlug.setValue(self.relative)

				# SET THE ".parameterU" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.parameterUSpecified:
					parameterUPlug = depNodeFn.findPlug("parameterU", True)
					parameterUPlug.setValue(self.parameterU)

				# SET THE ".parameterV" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.parameterVSpecified:
					parameterVPlug = depNodeFn.findPlug("parameterV", True)
					parameterVPlug.setValue(self.parameterV)

				# CONNECT THE NODES:
				inMeshPlug = depNodeFn.findPlug("inMesh", True)
				depNodeFn.setObject(meshDagPath.node())
				worldMeshPlug = depNodeFn.findPlug("worldMesh", True)
				worldMeshPlug = worldMeshPlug.elementByLogicalIndex(0)  # ASSUME THE *FIRST* INSTANCE OF THE MESH IS REQUESTED FOR MESH SHAPES.

				dgModifier = om.MDGModifier()
				dgModifier.connect(worldMeshPlug, inMeshPlug)
				dgModifier.doIt()

				# SET COMMAND RESULT AND RETURN:
				om.MPxCommand.setResult(self.pointOnMeshInfoName)

			# OTHERWISE, COMPUTE THE POINT-POSITION AND NORMAL, USING THE *FIRST* INSTANCE'S TRANSFORM:
			else:
				getPointAndNormal(meshDagPath, self.faceIndex, self.relative, self.parameterU, self.parameterV, point, normal)

		# WHEN THE SPECIFIED NODE IS A "TRANSFORM" OF A MESH SHAPE:
		elif meshDagPath.node().hasFn(om.MFn.kTransform) and meshDagPath.hasFn(om.MFn.kMesh):
			# WHEN NEITHER "-position/-p" NOR "-normal/-nr" ARE SPECIFIED, CREATE AND CONNECT A "pointOnMeshInfo" NODE AND RETURN ITS NODE NAME:
			if not self.positionSpecified and not self.normalSpecified:
				# CREATE THE NODE:
				self.nodeCreated = True
				meshDagPath.extendToShape()
				depNodeFn = om.MFnDependencyNode()

				if self.pointOnMeshInfoName == "":
					depNodeFn.create("pointOnMeshInfo")
				else:
					depNodeFn.create("pointOnMeshInfo", self.pointOnMeshInfoName)
				self.pointOnMeshInfoName = depNodeFn.name()

				# SET THE ".faceIndex" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.faceIndexSpecified:
					faceIndexPlug = depNodeFn.findPlug("faceIndex", True)
					faceIndexPlug.setValue(self.faceIndex)

				# SET THE ".relative" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.relativeSpecified:
					relativePlug = depNodeFn.findPlug("relative", True)
					relativePlug.setValue(self.relative)

				# SET THE ".parameterU" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.parameterUSpecified:
					parameterUPlug = depNodeFn.findPlug("parameterU", True)
					parameterUPlug.setValue(self.parameterU)

				# SET THE ".parameterV" ATTRIBUTE, IF SPECIFIED IN THE COMMAND:
				if self.parameterVSpecified:
					parameterVPlug = depNodeFn.findPlug("parameterV", True)
					parameterVPlug.setValue(self.parameterV)

				# CONNECT THE NODES:
				inMeshPlug = depNodeFn.findPlug("inMesh", True)
				depNodeFn.setObject(meshDagPath.node())
				worldMeshPlug = depNodeFn.findPlug("worldMesh", True)
				worldMeshPlug = worldMeshPlug.elementByLogicalIndex(meshDagPath.instanceNumber())

				dgModifier = om.MDGModifier()
				dgModifier.connect(worldMeshPlug, inMeshPlug)
				dgModifier.doIt()

				# SET COMMAND RESULT AND RETURN:
				om.MPxCommand.setResult(self.pointOnMeshInfoName)

			# OTHERWISE, COMPUTE THE POINT-POSITION AND NORMAL:
			else:
				getPointAndNormal(meshDagPath, self.faceIndex, self.relative, self.parameterU, self.parameterV, point, normal)

		# INVALID INPUT WHEN SPECIFIED/SELECTED NODE IS NOT A MESH NOR TRANSFORM:
		else:
			raise ValueError("Invalid type!  Only a mesh or its transform can be specified!")

		# SET THE RETURN VALUES OF THE COMMAND'S RESULT TO BE AN ARRAY OF FLOATS OUTPUTTING THE POSITION AND/OR NORMAL:
		result = om.MDoubleArray()
		if self.positionSpecified:
			result.append(point.x)
			result.append(point.y)
			result.append(point.z)
		if self.normalSpecified:
			result.append(normal.x)
			result.append(normal.y)
			result.append(normal.z)

		om.MPxCommand.setResult(result)

	# CALLED WHEN USER UNDOES THE COMMAND:
	def undoIt(self):
		# MERELY DELETE THE "pointOnMeshInfo" NODE THAT WAS CREATED, IF ONE WAS CREATED:
		if self.nodeCreated:
			deleteCmd = "delete " + self.pointOnMeshInfoName
			om.MGlobal.executeCommand(deleteCmd)

#
# MAIN CLASS DECLARATION FOR THE CUSTOM NODE:
#
class pointOnMeshInfoNode(om.MPxNode):
	id = om.MTypeId(0x00105480)
	aInMesh = None
	aFaceIndex = None
	aRelative = None
	aParameterU = None
	aParameterV = None
	aPosition = None
	aPositionX = None
	aPositionY = None
	aPositionZ = None
	aNormal = None
	aNormalX = None
	aNormalY = None
	aNormalZ = None

	aNurbsCurve = None

	def __init__(self):
		om.MPxNode.__init__(self)

	# FOR CREATING AN INSTANCE OF THIS NODE:
	@staticmethod
	def cmdCreator():
		return pointOnMeshInfoNode()

	# INITIALIZES THE NODE BY CREATING ITS ATTRIBUTES:
	@staticmethod
	def initialize():
		# CREATE AND ADD ".inMesh" ATTRIBUTE:
		inMeshAttrFn = om.MFnTypedAttribute()
		pointOnMeshInfoNode.aInMesh = inMeshAttrFn.create("inMesh", "im", om.MFnData.kMesh)
		inMeshAttrFn.storable = True
		inMeshAttrFn.keyable = False
		inMeshAttrFn.readable = True
		inMeshAttrFn.writable = True
		inMeshAttrFn.cached = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aInMesh)

		# CREATE AND ADD ".faceIndex" ATTRIBUTE:
		faceIndexAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aFaceIndex = faceIndexAttrFn.create("faceIndex", "f", om.MFnNumericData.kLong, 0)
		faceIndexAttrFn.storable = True
		faceIndexAttrFn.keyable = True
		faceIndexAttrFn.readable = True
		faceIndexAttrFn.writable = True
		faceIndexAttrFn.setMin(0)
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aFaceIndex)

		# CREATE AND ADD ".relative" ATTRIBUTE:
		relativeAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aRelative = relativeAttrFn.create("relative", "r", om.MFnNumericData.kBoolean, 1)
		relativeAttrFn.storable = True
		relativeAttrFn.keyable = True
		relativeAttrFn.readable = True
		relativeAttrFn.writable = True
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aRelative)

		# CREATE AND ADD ".parameterU" ATTRIBUTE:
		parameterUAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aParameterU = parameterUAttrFn.create("parameterU", "u", om.MFnNumericData.kDouble, 0.5)
		parameterUAttrFn.storable = True
		parameterUAttrFn.keyable = True
		parameterUAttrFn.readable = True
		parameterUAttrFn.writable = True
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aParameterU)

		# CREATE AND ADD ".parameterV" ATTRIBUTE:
		parameterVAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aParameterV = parameterVAttrFn.create("parameterV", "v", om.MFnNumericData.kDouble, 0.5)
		parameterVAttrFn.storable = True
		parameterVAttrFn.keyable = True
		parameterVAttrFn.readable = True
		parameterVAttrFn.writable = True
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aParameterV)

		# CREATE AND ADD ".positionX" ATTRIBUTE:
		pointXAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aPositionX = pointXAttrFn.create("positionX", "px", om.MFnNumericData.kDouble, 0.0)
		pointXAttrFn.storable = False
		pointXAttrFn.keyable = False
		pointXAttrFn.readable = True
		pointXAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aPositionX)

		# CREATE AND ADD ".positionY" ATTRIBUTE:
		pointYAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aPositionY = pointYAttrFn.create("positionY", "py", om.MFnNumericData.kDouble, 0.0)
		pointYAttrFn.storable = False
		pointYAttrFn.keyable = False
		pointYAttrFn.readable = True
		pointYAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aPositionY)

		# CREATE AND ADD ".positionZ" ATTRIBUTE:
		pointZAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aPositionZ = pointZAttrFn.create("positionZ", "pz", om.MFnNumericData.kDouble, 0.0)
		pointZAttrFn.storable = False
		pointZAttrFn.keyable = False
		pointZAttrFn.readable = True
		pointZAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aPositionZ)

		# CREATE AND ADD ".position" ATTRIBUTE:
		pointAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aPosition = pointAttrFn.create("position", "p", pointOnMeshInfoNode.aPositionX, pointOnMeshInfoNode.aPositionY, pointOnMeshInfoNode.aPositionZ)
		pointAttrFn.storable = False
		pointAttrFn.keyable = False
		pointAttrFn.readable = True
		pointAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aPosition)

		# CREATE AND ADD ".normalX" ATTRIBUTE:
		normalXAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aNormalX = normalXAttrFn.create("normalX", "nx", om.MFnNumericData.kDouble, 0.0)
		normalXAttrFn.storable = False
		normalXAttrFn.keyable = False
		normalXAttrFn.readable = True
		normalXAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aNormalX)

		# CREATE AND ADD ".normalY" ATTRIBUTE:
		normalYAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aNormalY = normalYAttrFn.create("normalY", "ny", om.MFnNumericData.kDouble, 0.0)
		normalYAttrFn.storable = False
		normalYAttrFn.keyable = False
		normalYAttrFn.readable = True
		normalYAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aNormalY)

		# CREATE AND ADD ".normalZ" ATTRIBUTE:
		normalZAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aNormalZ = normalZAttrFn.create("normalZ", "nz", om.MFnNumericData.kDouble, 0.0)
		normalZAttrFn.storable = False
		normalZAttrFn.keyable = False
		normalZAttrFn.readable = True
		normalZAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aNormalZ)

		# CREATE AND ADD ".normal" ATTRIBUTE:
		normalAttrFn = om.MFnNumericAttribute()
		pointOnMeshInfoNode.aNormal = normalAttrFn.create("normal", "n", pointOnMeshInfoNode.aNormalX, pointOnMeshInfoNode.aNormalY, pointOnMeshInfoNode.aNormalZ)
		normalAttrFn.storable = False
		normalAttrFn.keyable = False
		normalAttrFn.readable = True
		normalAttrFn.writable = False
		om.MPxNode.addAttribute(pointOnMeshInfoNode.aNormal)

		# DEPENDENCY RELATIONS FOR ".inMesh":
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aPosition)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aPositionX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aPositionY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aPositionZ)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aNormal)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aNormalX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aNormalY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aInMesh, pointOnMeshInfoNode.aNormalZ)

		# DEPENDENCY RELATIONS FOR ".faceIndex":
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aPosition)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aPositionX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aPositionY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aPositionZ)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aNormal)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aNormalX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aNormalY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aFaceIndex, pointOnMeshInfoNode.aNormalZ)

		# DEPENDENCY RELATIONS FOR ".relative":
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aPosition)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aPositionX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aPositionY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aPositionZ)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aNormal)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aNormalX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aNormalY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aRelative, pointOnMeshInfoNode.aNormalZ)

		# DEPENDENCY RELATIONS FOR ".parameterU":
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aPosition)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aPositionX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aPositionY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aPositionZ)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aNormal)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aNormalX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aNormalY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterU, pointOnMeshInfoNode.aNormalZ)

		# DEPENDENCY RELATIONS FOR ".parameterV":
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aPosition)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aPositionX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aPositionY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aPositionZ)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aNormal)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aNormalX)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aNormalY)
		om.MPxNode.attributeAffects(pointOnMeshInfoNode.aParameterV, pointOnMeshInfoNode.aNormalZ)

	# COMPUTE METHOD'S DEFINITION:
	def compute(self, plug, data):
		assert(isinstance(data.context(), om.MDGContext))
		assert(data.setContext(data.context()) == data)

		# DO THE COMPUTE ONLY FOR THE *OUTPUT* PLUGS THAT ARE DIRTIED:
		if plug == pointOnMeshInfoNode.aPosition or plug == pointOnMeshInfoNode.aPositionX or plug == pointOnMeshInfoNode.aPositionY or plug == pointOnMeshInfoNode.aPositionZ or plug == pointOnMeshInfoNode.aNormal or plug == pointOnMeshInfoNode.aNormalX or plug == pointOnMeshInfoNode.aNormalY or plug == pointOnMeshInfoNode.aNormalZ:
			# READ IN ".inMesh" DATA:
			inMeshDataHandle = data.inputValue(pointOnMeshInfoNode.aInMesh)
			inMesh = inMeshDataHandle.asMesh()

			# READ IN ".faceIndex" DATA:
			faceIndexDataHandle = data.inputValue(pointOnMeshInfoNode.aFaceIndex)
			faceIndex = faceIndexDataHandle.asInt()

			# READ IN ".relative" DATA:
			relativeDataHandle = data.inputValue(pointOnMeshInfoNode.aRelative)
			relative = relativeDataHandle.asBool()

			# READ IN ".parameterU" DATA:
			parameterUDataHandle = data.inputValue(pointOnMeshInfoNode.aParameterU)
			parameterU = parameterUDataHandle.asDouble()

			# READ IN ".parameterV" DATA:
			parameterVDataHandle = data.inputValue(pointOnMeshInfoNode.aParameterV)
			parameterV = parameterVDataHandle.asDouble()

			# GET THE POINT AND NORMAL:
			point = om.MPoint()
			normal = om.MVector()
			dummyDagPath = om.MDagPath()
			getPointAndNormal(dummyDagPath, faceIndex, relative, parameterU, parameterV, point, normal, inMesh)

			# WRITE OUT ".position" DATA:
			pointDataHandle = data.outputValue(pointOnMeshInfoNode.aPosition)
			pointDataHandle.set3Double(point.x, point.y, point.z)
			data.setClean(plug)

			# WRITE OUT ".normal" DATA:
			normalDataHandle = data.outputValue(pointOnMeshInfoNode.aNormal)
			normalDataHandle.set3Double(normal.x, normal.y, normal.z)
			data.setClean(plug)

			# The plug was successfully computed
			return self

		# Let the Maya parent class compute the plug
		return None

# INITIALIZES THE PLUGIN BY REGISTERING THE COMMAND AND NODE:
#
def initializePlugin(obj):
	plugin = om.MFnPlugin(obj)
	try:
		plugin.registerCommand("pointOnMesh", pointOnMeshCommand.cmdCreator)
	except:
		sys.stderr.write("Failed to register command\n")
		raise

	try:
		plugin.registerNode("pointOnMeshInfo", pointOnMeshInfoNode.id, pointOnMeshInfoNode.cmdCreator, pointOnMeshInfoNode.initialize)
	except:
		sys.stderr.write("Failed to register node\n")
		raise

#
# UNINITIALIZES THE PLUGIN BY DEREGISTERING THE COMMAND AND NODE:
#
def uninitializePlugin(obj):
	plugin = om.MFnPlugin(obj)
	try:
		plugin.deregisterCommand("pointOnMesh")
	except:
		sys.stderr.write("Failed to deregister command\n")
		raise

	try:
		plugin.deregisterNode(pointOnMeshInfoNode.id)
	except:
		sys.stderr.write("Failed to deregister node\n")
		raise


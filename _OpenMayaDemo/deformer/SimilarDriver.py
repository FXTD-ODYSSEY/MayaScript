# -*- coding:utf-8 -*-

import sys
import math
import json
import heapq
import traceback
from compiler.ast import flatten
from collections import OrderedDict
from itertools import combinations

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


import pymel.core as pm

kPluginNodeTypeName = "SimilarDriver"

SimilarDriverId = OpenMaya.MTypeId(0x187606)

# Node definition
class SimilarDriver(OpenMayaMPx.MPxNode):
    # class variables
    weight   = OpenMaya.MObject()
    envelope = OpenMaya.MObject()
    border   = OpenMaya.MObject()
    thersold   = OpenMaya.MObject()

    joint       = OpenMaya.MObject()
    jntMatrix   = OpenMaya.MObject()
    reJntMatrix = OpenMaya.MObject()
    
    baseExpPt   = OpenMaya.MObject()
    reExpPt     = OpenMaya.MObject()
    expPt       = OpenMaya.MObject()
    expGrp      = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def exceptionHandler(fn):
        """异常装饰器"""
        def wrapper(*args,**kwargs):
            try:
                ret = fn(*args,**kwargs)
                return ret
            except:
                self = args[0]
                print ("ERROR NODE: " + self.name())
                traceback.print_exc()
                return OpenMaya.kUnknownParameter
        return wrapper
        
    def calcPtInfo(self,pt_jnt,pt_1,pt_2,return_val="all"):
        vec_1     = pt_jnt - pt_1
        vec_2     = pt_jnt - pt_2
        vec_1_len = vec_1.length()
        vec_2_len = vec_2.length()
        # angle = vec_1*vec_2/(vec_1_len*vec_2_len)


        if return_val == "all":
            return {
                "vec_1_len":vec_1_len,
                "vec_2_len":vec_2_len,
                "vec_1":vec_1,
                "vec_2":vec_2,
            }
        # elif return_val == "edge":
        #     return {
        #         "vec_2_len":vec_2_len,
        #         "angle":angle,
        #     }
        # elif return_val == "angle":
        #     return {
        #         "angle":angle,
        #     }

    @exceptionHandler
    def compute(self,plug,dataBlock):
        if ( plug == self.weight ): 
            # print "============%s===============" % self.name()
            # NOTE 获取输出阈值 
            envelope = dataBlock.inputValue(self.envelope).asFloat()
            thersold = dataBlock.inputValue(self.thersold).asFloat()
            border = dataBlock.inputValue(self.border).asFloat()

            jntMatrix = dataBlock.inputValue( self.jntMatrix ).asMatrix()
            jointPoint = OpenMaya.MPoint(jntMatrix(3,0),jntMatrix(3,1),jntMatrix(3,2))
            
            # ! -------------------------------------------
            # !         获取骨骼位置和表情点的位置
            # ! -------------------------------------------
            expGrpPlugs = OpenMaya.MPlug(self.thisMObject(), self.expGrp)
            expGrpArrayHandle = dataBlock.inputArrayValue( self.expGrp )
            
            weight_list = []
            samll_list = []

            data_list = []
            index_list = OpenMaya.MIntArray()
            expGrpPlugs.getExistingArrayAttributeIndices(index_list)

            # NOTE 获取最后的序号值
            last_idx = index_list[index_list.length()-1]
            el_count = expGrpPlugs.elementByLogicalIndex(last_idx).child(self.expPt).numElements()
            
            # NOTE 如果最后的序号没有元素 去掉最后一个元素
            index_list = list(index_list) if el_count else list(index_list)[:-1]
            weight_list = [0 for j in range(index_list[-1])]
            exp_pt_list = []
            for idx in (index_list):
                expGrpPlug = expGrpPlugs.elementByLogicalIndex(idx)
                expGrpArrayHandle.jumpToElement(idx)
                expGrpHandle = expGrpArrayHandle.inputValue()

                expPtArrayHandle = OpenMaya.MArrayDataHandle(expGrpHandle.child(self.expPt))
                expPtArrayHandle.jumpToElement(0)
                
                expPoint = OpenMaya.MPoint(*expPtArrayHandle.inputValue().asFloat3())
                
                length = (jointPoint - expPoint).length()

                data = {
                    "idx":idx,
                    "len":length,
                    "expPoint":expPoint,
                    "expGrpPlug":expGrpPlug,
                }
                # print data["expGrpPlug"].child(self.expPt)[0].source().name().replace("editPoints","cv"),round(data["len"],2)
                data_list.append(data)

                # NOTE 添加 基准 的数据计算 base_weight
                if idx == 0:
                    samll_list.append(data)
                
                    
 
            # ! -------------------------------------------
            # !         过滤出最相近的两个点
            # ! -------------------------------------------
            # NOTE 取出长度最小的三个表情点
            for data in heapq.nsmallest(3,data_list,key=lambda s: s['len']):
                # print data["expGrpPlug"].child(self.expPt)[0].source().name().replace("editPoints","cv"),round(data["len"],2)

                # NOTE 判断 idx 是否有重复的 避免重复添加 基准data 
                for _data in samll_list:
                    if data["idx"] == _data["idx"]:
                        break
                else:
                    samll_list.append(data)

            length_list = [data['len'] for data in samll_list]
            min_value = min(length_list)

            remap_list = self.minMaxNorm(length_list,min_val=0 if min_value > 0.1 else min_value,max_val=max(length_list))
            
            base_weight = 1
            for data,remap in zip(samll_list,remap_list):
                idx = data['idx']

                weight = 1 if remap < thersold else 1 - remap 
                # print "weight",weight
                if idx == 0:
                    base_weight = remap
                    basePoint = data['expPoint']
                else:
                    expPoint = data['expPoint']

                    info = self.calcPtInfo(basePoint,jointPoint,expPoint)
      
                    jnt_len = info["vec_1_len"]
                    exp_len = info["vec_2_len"]
                    
                    weight *= base_weight 
                    if jnt_len < thersold:
                        weight = 0
                    elif data['len'] < thersold:
                        weight = 1
                    # else:
                    #     angle = info["vec_1"]*info["vec_2"]/(jnt_len*exp_len)
                    #     reflect_len = jnt_len * math.cos(angle)
                    #     _weight = reflect_len / exp_len
                    #     _weight = _weight if _weight <= 1 else 1/_weight
                    #     weight *= _weight
                    #     # print self.name(),math.cos(angle),weight

                    weight_list[idx-1] = 0 if weight < border else (weight - border)/(1 - border)

                
            weight_list = [weight * envelope 
                           if weight * envelope < 1 else 1
                           for weight in self.rangeValueFilter(weight_list,2)]

            # NOTE 只保留最大值
            max_value = max(weight_list)
            weight_list = [0 if weight<max_value else weight for weight in weight_list]

            # NOTE 遍历输出权重值
            weightArrayHandle = dataBlock.outputArrayValue(self.weight)
            weightBuilder     = weightArrayHandle.builder()
            for j,weight in enumerate(weight_list):
                weightHandle = weightBuilder.addElement(j)
                weightHandle.setFloat(weight)
                weightHandle.setClean()

            # NOTE 设置输出数值
            weightArrayHandle.set(weightBuilder)
            weightArrayHandle.setAllClean()
            dataBlock.setClean( plug )

        else:
            return OpenMaya.kUnknownParameter
    
    # def ratioFilter(self,val):
    #     u"""
    #     ratioFilter
        
    #     将数值限定到 0 - 1 的区间中
    #     1 - 2 区间的数值会翻转到 0 - 1 区间上
    #     数值在 0 - 2 区间以外则只取 0 和 2 的峰值进行处理

    #     Arguments:
    #         val {float} -- 数据
        
    #     Returns:
    #         [float] -- 输出过滤值
    #     """

    #     # NOTE 限制输出值的范围在 0 - 2 之间超出则不考虑
    #     val = 0 if val > 2 else val
    #     result = 0 if val < 0 else val
    #     # NOTE 将大于1的值转换为 0 - 1 区间中
    #     result = (2 - result) if result > 1 else result
    #     return round(result,3)
    
    def rangeValueFilter(self,value_list,filter_num=1):
        u"""
        rangeValueFilter 
        
        将输出数值按最大进行过滤映射 重映射不会导致数值跳动
        
        Arguments:
            value_list {list} -- 数据数组
        
        Keyword Arguments:
            filter_num {int} -- 过滤后保留数值的个数 (default: {1})
        
        Returns:
            [list] -- 过滤数组
        """
        filter_num += 1
        if filter_num < 2:return

        # NOTE 获取数组中最大的 filter_num 数组
        largest_list = heapq.nlargest(filter_num, value_list)
                    
        # NOTE min(largest_list) - 取出上面数组中的最小值最为映射最小值
        # NOTE        最大区域
        # NOTE |=======|←-→| 分离出最大区域
        # NOTE |←---------→| 重新将最大区域的数值按 min(largest_list) 到 1 映射
        result_list = self.minMaxNorm(value_list,min_val=min(largest_list),max_val=1)
        # NOTE 将最大区域外的数值全部归零(上面的操作会变为负数)
        result_list = [0.0 if value < 0.01 else round(value,3) for value in result_list]
        # for i,value in enumerate(result_list):
        #     result_list[i] = 0.0 if value < 0.01 else round(value,3)

        return result_list

    def minMaxNorm(self,data,min_val=None,max_val=None):
        u""" min-max标准化 """
        n = len(data)
        if n < 1:
            raise ValueError(u'数据为空')
        fl_data = flatten(data)
        min_val = min(fl_data) if min_val == None else min_val
        max_val = max(fl_data) if max_val == None else max_val
        # NOTE 如果最大最小值一样 返回data
        if min_val == max_val:
            # NOTE 除最大值之外全部归零
            for i,val in enumerate(fl_data): 
                if val < max_val: 
                    fl_data[i] = 0.0
            return fl_data
        else:
            return [float(val - min_val)/(max_val - min_val) for val in fl_data]

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( SimilarDriver() )

# initializer
def nodeInitializer():

    mAttr = OpenMaya.MFnMatrixAttribute()
    tAttr = OpenMaya.MFnTypedAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # ! ------------------------------------------------------------------------- ! #

    SimilarDriver.jntMatrix = mAttr.create("jntMatrix", "jm")
    # NOTE NodeEditor 显示
    mAttr.setKeyable(1)
    mAttr.setWritable(1)

    # ! ------------------------------------------------------------------------- ! #

    SimilarDriver.reJntMatrix = mAttr.create("reJntMatrix", "cjm")
    # NOTE 设置为数组类型
    mAttr.setArray(1)
    mAttr.setUsesArrayDataBuilder(1)
    # NOTE NodeEditor 显示
    mAttr.setKeyable(1)
    mAttr.setWritable(1)

    # ! ------------------------------------------------------------------------- ! #

    # NOTE 获取骨骼数据组
    SimilarDriver.joint = cAttr.create("joint", "jnt")
    cAttr.addChild(SimilarDriver.jntMatrix)
    cAttr.addChild(SimilarDriver.reJntMatrix)

    # ! ------------------------------------------------------------------------- ! #

    # NOTE 打包空间点数据组
    SimilarDriver.expPt = nAttr.create("expPt", "ept",OpenMaya.MFnNumericData.k3Float)

    # NOTE 设置为数组类型
    nAttr.setArray(1)
    nAttr.setUsesArrayDataBuilder(1)
    # NOTE NodeEditor 显示
    nAttr.setKeyable(1)
    nAttr.setWritable(1)

    # ! ------------------------------------------------------------------------- ! #
 
    SimilarDriver.expGrp = cAttr.create("expGrp", "epg")
    cAttr.setArray(1)
    cAttr.setUsesArrayDataBuilder(1)
    cAttr.addChild(SimilarDriver.expPt)

    # ! ------------------------------------------------------------------------- ! #

    SimilarDriver.envelope = nAttr.create("envelope", "en",OpenMaya.MFnNumericData.kFloat)
    # NOTE NodeEditor 显示
    nAttr.setKeyable(1)
    nAttr.setWritable(1)
    nAttr.setDefault(1.0)

    # ! ------------------------------------------------------------------------- ! #

    SimilarDriver.border = nAttr.create("border", "bd",OpenMaya.MFnNumericData.kFloat)
    # NOTE NodeEditor 显示
    nAttr.setKeyable(1)
    nAttr.setWritable(1)
    nAttr.setDefault(0.5)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)

    # ! ------------------------------------------------------------------------- ! #

    SimilarDriver.thersold = nAttr.create("thersold", "dt",OpenMaya.MFnNumericData.kFloat)
    # NOTE NodeEditor 显示
    nAttr.setKeyable(1)
    nAttr.setWritable(1)
    nAttr.setDefault(0.02)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    
    # ! ------------------------------------------------------------------------- ! #
    
    # NOTE output
    SimilarDriver.weight = nAttr.create( "weight", "w", OpenMaya.MFnNumericData.kFloat, 0.0 )
    nAttr.setStorable(1)
    nAttr.setWritable(1)
    nAttr.setArray(1)
    nAttr.setUsesArrayDataBuilder(1)

    # NOTE 添加属性
    SimilarDriver.addAttribute( SimilarDriver.weight )
    SimilarDriver.addAttribute( SimilarDriver.joint )
    SimilarDriver.addAttribute( SimilarDriver.expGrp )
    SimilarDriver.addAttribute( SimilarDriver.envelope )
    SimilarDriver.addAttribute( SimilarDriver.thersold )
    SimilarDriver.addAttribute( SimilarDriver.border )

    # NOTE 受影响的属性
    SimilarDriver.attributeAffects( SimilarDriver.joint, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.jntMatrix, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.reJntMatrix, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.expGrp, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.expPt, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.envelope, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.thersold, SimilarDriver.weight )
    SimilarDriver.attributeAffects( SimilarDriver.border, SimilarDriver.weight )
    
# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, SimilarDriverId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( SimilarDriverId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
        raise
    

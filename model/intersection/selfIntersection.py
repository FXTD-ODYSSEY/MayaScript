# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-09 20:54:46'

"""
自穿插面查找
速度贼慢 | 有很大优化空间
"""

from maya import cmds
from maya import OpenMaya


    
def run():
    thersold = 0.0001

    face_list = OpenMaya.MSelectionList()

    selection_list = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection_list)

    path = OpenMaya.MDagPath()
    comp = OpenMaya.MObject()
    util = OpenMaya.MScriptUtil(0)
    space = OpenMaya.MSpace.kWorld

    for num in range(selection_list.length()):
        selection_list.getDagPath(num,path,comp)
        node = OpenMaya.MFnDagNode(path)
        # bbox = node.boundingBox()
        # mesh = OpenMaya.MFnMesh(path)
        
        itr_1 = OpenMaya.MItMeshPolygon(path)
        itr_2 = OpenMaya.MItMeshPolygon(path)

        cmds.progressWindow(	title=u'寻面中',
					progress=0,
					status=u'寻面中...',
					isInterruptable=True )
        amount = 0.0
        while not itr_1.isDone():
            
            if cmds.progressWindow( query=True, isCancelled=True ) :
    		    break

            amount += 1.0
            progress = amount/itr_1.count()*100
            cmds.progressWindow( edit=True, progress=progress)


            count = itr_1.index()

            point_list_1 = OpenMaya.MPointArray()
            index_list_1 = OpenMaya.MIntArray()
            itr_1.getTriangles(point_list_1,index_list_1,space)
            tri_num_1 = point_list_1.length()/3

            while count < itr_2.count()-1 :
                count += 1
                itr_2.setIndex(count,util.asIntPtr())

                point_list_2 = OpenMaya.MPointArray()
                index_list_2 = OpenMaya.MIntArray()
                itr_2.getTriangles(point_list_2,index_list_2,space)
                tri_num_2 = point_list_2.length()/3

                # print "index: ",itr_1.index()," =============== ",itr_2.index()

                for i in range(tri_num_1):
                    # Note 获取三角面的点 和 法线
                    P0_1 = point_list_1[i*3]
                    P1_1 = point_list_1[i*3+1]
                    P2_1 = point_list_1[i*3+2]
                    u_1 = P0_1 - P1_1 
                    v_1 = P0_1 - P2_1 
                    n_1 = u_1 ^ v_1
                    n_1.normalize()

                    for j in range(tri_num_2):

                        # Note 获取另一个 三角面的点 和 法线
                        P0_2 = point_list_2[j*3]
                        P1_2 = point_list_2[j*3+1]
                        P2_2 = point_list_2[j*3+2]
                        u_2 = P0_2 - P1_2
                        v_2 = P0_2 - P2_2
                        n_2 = u_2 ^ v_2
                        n_2.normalize()
                        
                        u = n_1 ^ n_2
                        ax = abs(u.x)
                        ay = abs(u.y)
                        az = abs(u.z)
                        # Note 面平行 跳过
                        if (ax+ay+az) < thersold:
                            continue
                        
                        v1 = n_2*(P0_1 - P0_2)
                        v2 = n_2*(P1_1 - P0_2)
                        v3 = n_2*(P2_1 - P0_2)
                        
                        v_count = 0
                        if abs(v1) < thersold:
                            v_count += 1
                        if abs(v2) < thersold:
                            v_count += 1
                        if abs(v3) < thersold:
                            v_count += 1
                        # Note 如果有两个点重合 跳过
                        if v_count >= 1 :
                            continue
                        
                        
                        # Note 不同 side 说明与三角形与平面穿插
                        if not (v1>0 and v2>0 and v3>0) or not (v1<0 and v2<0 and v3<0):
                            # Note http://geomalgorithms.com/a06-_intersect-2.html
                            def getHitPoint(P1_1,P0_1):
                                dir1 = P1_1 - P0_1
                                w = P0_1 - P0_2
                                a = -w*n_2
                                b1 = dir1*n_2
                                r1 = a / b1
                                return P0_1 + dir1*r1 
                            # Note P0_1 为穿插点
                            if (v1>0 and v2<0 and v3<0) or (v1<0 and v2>0 and v3>0):
                                hit_1 = getHitPoint(P1_1,P0_1)
                                hit_2 = getHitPoint(P2_1,P0_1)
                            # Note P1_1 为穿插点
                            elif (v1<0 and v2>0 and v3<0) or (v1>0 and v2<0 and v3>0):
                                hit_1 = getHitPoint(P0_1,P1_1)
                                hit_2 = getHitPoint(P2_1,P1_1)
                            # Note P2_1 为穿插点
                            elif (v1<0 and v2<0 and v3>0) or (v1>0 and v2>0 and v3<0):
                                hit_1 = getHitPoint(P0_1,P2_1)
                                hit_2 = getHitPoint(P1_1,P2_1)
                            else:
                                continue

                            
                            # Note 判断是否在三角面当中
                            def triangleInside(hit):
                                u = P1_2 - P0_2
                                v = P2_2 - P0_2
                                uu = u*u
                                uv = u*v
                                vv = v*v
                                w = hit - P0_2
                                wu = w*u
                                wv = w*v
                                D = uv * uv - uu * vv
                                s = (uv * wv - vv * wu) / D
                                t = (uv * wu - uu * wv) / D
                                if (s <= 0.0 or s >= 1.0) or (t <= 0.0 or (s + t) >= 1.0) :
                                    return False
                                return True

                            # if itr_1.index() == 65:
                            #     # Note 可视化
                            #     loc = cmds.spaceLocator(a=1)[0]
                            #     cmds.setAttr("%s.tx"%loc,hit_1.x)
                            #     cmds.setAttr("%s.ty"%loc,hit_1.y)
                            #     cmds.setAttr("%s.tz"%loc,hit_1.z)
                            #     loc = cmds.spaceLocator(a=1)[0]
                            #     cmds.setAttr("%s.tx"%loc,hit_2.x)
                            #     cmds.setAttr("%s.ty"%loc,hit_2.y)
                            #     cmds.setAttr("%s.tz"%loc,hit_2.z)
                                # print triangleInside(hit_1)  
                                # print triangleInside(hit_2)

                            if triangleInside(hit_1) or triangleInside(hit_2):

                                # print itr_1.index(),":",itr_2.index()

                                face_list.add("%s.f[%s]"%(node.fullPathName(),itr_1.index()))
                                face_list.add("%s.f[%s]"%(node.fullPathName(),itr_2.index()))
                                # 跳出当前的面循环
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break

            itr_1.next()

    OpenMaya.MGlobal.setActiveSelectionList(face_list)
    cmds.progressWindow(endProgress=1)

        
# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-24 09:17:53'

import pymel.core as pm

""" 
根据当前通道盒的选择断开链接
"""

def disAttr():
    # NOTE 获取当前通道盒选择的属性
    attr_list = pm.channelBox('mainChannelBox',q=1,sma=1)
    # NOTE 没有选择跳过执行
    if not attr_list:
        return

    for sel in pm.ls(sl=1):
        for attr in attr_list:
            if not hasattr(sel,attr):
                continue
        
            attr = pm.PyNode("%s.%s"%(sel,attr))
            des = pm.PyNode(pm.connectionInfo(attr,ged=1))
            if des == attr:
                attr.disconnect()
            else:
                # NOTE 如果获取的属性不相等说明是 Translate类似集合 的上层链接
                src = des.listConnections(d=0,s=1,p=1)[0]
                des.disconnect()
                for d_attr,s_attr in zip(des.getChildren(),src.getChildren()):
                    if d_attr != attr:
                        s_attr.connect(d_attr)

if __name__ == "__main__":
    disAttr()
# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-26 12:41:54'

"""
https://stackoverflow.com/questions/29708445/how-do-i-make-a-contextmanager-with-a-loop-inside
"""

from maya import cmds
import traceback

def loop(seq,title=''):
    cmds.progressWindow(	
        title=title ,
        progress=0.0,
        isInterruptable=True )
    total = len(seq)
    for i,item in enumerate(seq):
        try:
            if cmds.progressWindow( query=True, isCancelled=True ) : break
            cmds.progressWindow( e=True, progress=float(i)/total*100 )
            yield item  # with body executes here
        except:
            traceback.print_exc()
            cmds.progressWindow(ep=1)
    cmds.progressWindow(ep=1)
   
for i in loop(range(5000)):
    print i
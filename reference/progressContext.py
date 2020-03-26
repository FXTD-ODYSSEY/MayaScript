# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-26 12:41:54'

"""
https://stackoverflow.com/questions/29708445/how-do-i-make-a-contextmanager-with-a-loop-inside
"""

from contextlib import contextmanager
from maya import cmds
import traceback

def loop(seq):
    total = len(seq)
    for i in seq:
        try:
            if cmds.progressWindow( query=True, isCancelled=True ) : break
            cmds.progressWindow( e=True, progress=float(i)/total*100 )
            yield i  # with body executes here
        except:
            traceback.print_exc()

@contextmanager
def progressWindow(title="",status="",data=[]) :
    cmds.progressWindow(	
        title=title ,
        progress=0.0,
        isInterruptable=True )
    try :
        yield loop(data)
    except:
        traceback.print_exc()
    finally :
        cmds.progressWindow(ep=1)
   
with progressWindow(data=range(5000)) as data:
    for i in data:
        print i
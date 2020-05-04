# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 10:13:42'

"""
https://stackoverflow.com/questions/481692/can-a-lambda-function-call-itself-recursively-in-python
NOTE Auto Find the Git Repo base on the .git directory
"""

import os

def getGitRepo(p = __file__):
    p = p if os.path.isdir(p) else os.path.dirname(p)
    for f in os.listdir(p):
        if f == '.git':
            return p
    else:
        if os.path.dirname(p) != p:
            return getGitRepo(os.path.dirname(p)) 

repo = getGitRepo()

print ("%-25s" % "full code repo:",repo)

def getGitRepo(p=__file__):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo()

print ("%-25s" % "one line repo:",repo)

repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()

print ("%-25s" % "recusive lambda repo:",repo)

# NOTE ---------------------------------------------------------------

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets


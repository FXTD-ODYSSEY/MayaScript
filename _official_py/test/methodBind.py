# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 14:54:20'

"""
https://www.liaoxuefeng.com/wiki/897692888725344/923030542875328
"""

from types import MethodType

class Student(object):
    pass
s = Student()
s2 = Student()

def set_score(self, score = -1):
    print ('score',score)
# Student.set_score = MethodType(set_score, None, Student)


setattr(Student,"set_score",set_score)

s2.set_score(2)


class A(object):
  def method(self, other):
    print (self)
 
class B(object): pass
 
B.method = MethodType(A().method, None, B)
B().method() # print both A and B instances

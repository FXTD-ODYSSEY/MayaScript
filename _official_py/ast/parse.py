# -*- coding: utf-8 -*-
"""
TODO
https://stackoverflow.com/a/30037835
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-30 23:04:31'

import ast
import os
import astunparse
import astpretty

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, 'src.py')
DST = os.path.join(DIR, 'dst.py')

with open(SRC, 'r') as f:
    data = f.read()

class NodeVisitor(ast.NodeTransformer):
    def visit_Assign(self, node): # 修改操作符
        obj = node.value.func
        if isinstance(obj,ast.Name):
            print(obj.id)

        obj.id = "test.asd"
        return node
        # if isinstance(node.op, ast.Mod):
        #     node.op = ast.Add()
        self.generic_visit(node) # 遍子节点
        
    # def visit_alias(self, node):
    #     print(node.name)
    #     return
    #     self.generic_visit(node)
    
    # def generic_visit(self, node):
    #     print(node)
    #     return super(NodeVisitor, self).generic_visit(node)
        

if __name__ == "__main__":
        
    f_ast = ast.parse(data)
    visitor = NodeVisitor()
    visitor.visit(f_ast)

    source = astunparse.unparse(f_ast)
    with open(DST,'w') as f:
        f.write(source)

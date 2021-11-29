# -*- coding: utf-8 -*-
"""
https://medium.com/nothingaholic/depth-first-search-vs-breadth-first-search-in-python-81521caa8f44
广度优先遍历
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-23 20:37:16'

import pymel.core as pm

    
def breadth_search(nodes):
    nodes = nodes if isinstance(nodes,list) else [nodes]
    visited = nodes[:]
    queue = nodes[:]
    while queue:
        node = queue.pop(0)
        yield node
        for neighbor in node.getChildren(type="transform"):
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)


if __name__ == "__main__":
    for node in breadth_search(pm.selected()):
        print(node)


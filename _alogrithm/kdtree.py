#!/usr/bin/python
# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 19:27:02'

"""
https://gumroad.com/l/skinningTools_PL
自动查询相邻的顶点
"""

""" KDTree implementation.

Features:

- nearest neighbours search

Matej Drame [matej.drame@gmail.com]
"""

__version__ = "1r11.1.2010"
__all__ = ["KDTree"]

def square_distance(pointA, pointB):
    # squared euclidean distance
    distance = 0
    dimensions = len(pointA) # assumes both points have the same dimensions
    for dimension in range(dimensions):
        distance += (pointA[dimension] - pointB[dimension])**2
    return distance

class KDTreeNode():
    def __init__(self, point, left, right):
        self.point = point
        self.left = left
        self.right = right
    
    def is_leaf(self):
        return (self.left == None and self.right == None)

class KDTreeNeighbours():
    """ Internal structure used in nearest-neighbours search.
    """
    def __init__(self, query_point, t):
        self.query_point = query_point
        self.t = t # neighbours wanted
        self.largest_distance = 0 # squared
        self.current_best = []

    def calculate_largest(self):
        if self.t >= len(self.current_best):
            self.largest_distance = self.current_best[-1][1]
        else:
            self.largest_distance = self.current_best[self.t-1][1]

    def add(self, point):
        sd = square_distance(point, self.query_point)
        # run through current_best, try to find appropriate place
        for i, e in enumerate(self.current_best):
            if i == self.t:
                return # enough neighbours, this one is farther, let's forget it
            if e[1] > sd:
                self.current_best.insert(i, [point, sd])
                self.calculate_largest()
                return
        # append it to the end otherwise
        self.current_best.append([point, sd])
        self.calculate_largest()
    
    def get_best(self):
        return [element[0] for element in self.current_best[:self.t]]
        
class KDTree():
    """ KDTree implementation.
    
        Example usage:
        
            from kdtree import KDTree
            
            data = <load data> # iterable of points (which are also iterable, same length)
            point = <the point of which neighbours we're looking for>
            
            tree = KDTree.construct_from_data(data)
            nearest = tree.query(point, t=4) # find nearest 4 points
    """
    
    def __init__(self, data):
        def build_kdtree(point_list, depth):
            # code based on wikipedia article: http://en.wikipedia.org/wiki/Kd-tree
            if not point_list:
                return None

            # select axis based on depth so that axis cycles through all valid values
            axis = depth % len(point_list[0]) # assumes all points have the same dimension

            # sort point list and choose median as pivot point,
            # TODO: better selection method, linear-time selection, distribution
            point_list.sort(key=lambda point: point[axis])
            median = len(point_list)/2 # choose median

            # create node and recursively construct subtrees
            node = KDTreeNode(point=point_list[median],
                              left=build_kdtree(point_list[0:median], depth+1),
                              right=build_kdtree(point_list[median+1:], depth+1))
            return node
        
        self.root_node = build_kdtree(data, depth=0)
    
    @staticmethod
    def construct_from_data(data):
        tree = KDTree(data)
        return tree

    def query(self, query_point, t=1):
        statistics = {'nodes_visited': 0, 'far_search': 0, 'leafs_reached': 0}
        
        def nn_search(node, query_point, t, depth, best_neighbours):
            if node == None:
                return
            
            #statistics['nodes_visited'] += 1
            
            # if we have reached a leaf, let's add to current best neighbours,
            # (if it's better than the worst one or if there is not enough neighbours)
            if node.is_leaf():
                #statistics['leafs_reached'] += 1
                best_neighbours.add(node.point)
                return
            
            # this node is no leaf
            
            # select dimension for comparison (based on current depth)
            axis = depth % len(query_point)
            
            # figure out which subtree to search
            near_subtree = None # near subtree
            far_subtree = None # far subtree (perhaps we'll have to traverse it as well)
            
            # compare query_point and point of current node in selected dimension
            # and figure out which subtree is farther than the other
            if query_point[axis] < node.point[axis]:
                near_subtree = node.left
                far_subtree = node.right
            else:
                near_subtree = node.right
                far_subtree = node.left

            # recursively search through the tree until a leaf is found
            nn_search(near_subtree, query_point, t, depth+1, best_neighbours)

            # while unwinding the recursion, check if the current node
            # is closer to query point than the current best,
            # also, until t points have been found, search radius is infinity
            best_neighbours.add(node.point)
            
            # check whether there could be any points on the other side of the
            # splitting plane that are closer to the query point than the current best
            if (node.point[axis] - query_point[axis])**2 < best_neighbours.largest_distance:
                #statistics['far_search'] += 1
                nn_search(far_subtree, query_point, t, depth+1, best_neighbours)
            
            return
        
        # if there's no tree, there's no neighbors
        if self.root_node != None:
            neighbours = KDTreeNeighbours(query_point, t)
            nn_search(self.root_node, query_point, t, depth=0, best_neighbours=neighbours)
            result = neighbours.get_best()
        else:
            result = []
        
        #print statistics
        return result

# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 19:22:18'

"""
https://github.com/pinkwerks/Maya-Scripts/blob/master/scripts/delaunay.py
根据输入的顶点生成拓扑结构
https://baike.baidu.com/item/Delaunay三角剖分算法
"""

##
##  DELAUNAY MATH
##  Classes to calculate Delaunay triangulations via mathematical operations
##
##  Based on the algorithm by Paul Bourke
## (http://local.wasp.uwa.edu.au/~pbourke/papers/triangulate/index.html)
##
##  Created by: Daniel da Rocha
##  Last modified: 21.06.09 by Daniel da Rocha
##  Modified by pinkwerks

import maya.cmds as cmds
import math
import datetime

##Usage:
##Create a set of points and store the names of the locators in a list.
##This can be done both by yourself or by using the Qhull class's point generation methods.
##Then create an instance of this class, passing this points list as an argument:
##d = Denaulay(points)
##
##To calculate, call the triangulate() method

### TLDR;Usage
"""
from pymel.core import *
execfile(r"C:/Users/pink/Documents/GitHub/maya/scripts/delaunay.py")
import random

locatorNames = []

for x in range(5):
    x = random.random();
    y = random.random();
    sl = spaceLocator(p=[x, y, 0])
    locatorNames.append(sl.name())

d = Delaunay(locatorNames);

d.triangulate()
"""

class Delaunay:
    def __init__(self, points):
        "Constructor: gets a set of locators and create the appropriate attributes from it"
        #save names of locators
        self.locators = points
        #save coordinates of locators
        self.vertices = [cmds.pointPosition(i) for i in points]
        #check number of original points
        self.numPoints = len(points)
        #feedback:
        print("New instance of the DelaunayMath class created.")
        print(">>", self.numPoints, "points.")

    def triangulate(self, outType="curves", timer=0):
        "Makes all calculation. You can specify the output type (curves or faces) and if you want to set a timer to see consumed time in the operation"

        #check if you want to display time consumed for the operation:
        if timer: currTime = datetime.datetime.now()

        #create an empty triangle list
        triangles = []
        #and en empty list to store vertexes in order
        vertex = []

        ##we need to start with a supertriangle which encompasses all the points
        ##this is done by getting the minimum and maximum bounds of all points
        ##and by adding a triangle to the triangles list which is a tad bigger than this bounds
        #copy the vertices list
        vs = self.vertices
        vertex.extend(vs)
        #make a series of operations to find minimum and maximum x and y values
        xmin = vs[0][0]
        ymin = vs[0][1]
        xmax = xmin
        ymax = ymin
        for i in range(self.numPoints):
            if vs[i][0] < xmin: xmin = vs[i][0]
            if vs[i][0] > xmax: xmax = vs[i][0]
            if vs[i][1] < ymin: ymin = vs[i][1]
            if vs[i][1] > ymax: ymax = vs[i][1]
        #get min and max distances
        dx = xmax-xmin
        dy = ymax-ymin
        if dx > dy:
            dmax = dx
        else:
            dmax = dy
        #get mid points of these distances
        xmid = (xmax+xmin)/2
        ymid = (ymax+ymin)/2

        #calculate the coordinates of the vertices of the supertriangle
        #and add them to the end of the vertex list
        #and add this triangle to the triangles list (it is the first)
        v1x = xmid - 2*dmax
        v1y = ymid - dmax
        vertex.append([v1x, v1y])
        v2x = xmid
        v2y = ymid + 2*dmax
        vertex.append([v2x, v2y])
        v3x = xmid + 2*dmax
        v3y = ymid - dmax
        vertex.append([v3x, v3y])
        triangles.append([self.numPoints,self.numPoints+1,self.numPoints+2])

        ##having already one triangle in the triangles list, we can start adding points
        ##and re-triangulate everytime we need

        #progress window > initialize before the loop
        cmds.progressWindow(title='Creating Delaunay regions...', #here you input your message for the progress window/can be anything
                            minValue=0,
                            maxValue=self.numPoints,    # this is imporant: when will the progress be 100%?
                            status='Points left: %d' % self.numPoints,  # here is some status message /anything you want
                            isInterruptable=True )

        #Include each point one at a time into the existing triangulations
        for i in range(len(vertex)):
            #if i is more than the original number of points, stop loop
            #cos then it is a vertex of the supertriangle, and we don't need to calculate them
            if i >= self.numPoints: break
            #get current point i coordinates
            p = vertex[i]
            #Set up the edge buffer.
            #If the point (x,y) lies inside the circumcircle formed by each triangle,
            #then the three edges of that triangle are added to the edge buffer.
            edges = []

            #create a copy of the triangles list to loop through
            tcopy = []
            tcopy.extend(triangles)
            #loop through the triangles to check the points
            for t in tcopy:
                #if the triangle is composed by the vertex in question (i), skip
                if i in t: continue
                #convert the triangle vertices to a list of coordinates
                tri=[ [vertex[k][0], vertex[k][1]] for k in t ]
                #check if the point i is in the circle formed by this triangle
                ic = self.inCircle(point=[p[0], p[1]], triangle=tri)
                if ic:
                    #in case ic == true:
                    #store the edges in the edges list
                    edges.append([t[0], t[1]])
                    edges.append([t[1], t[2]])
                    edges.append([t[2], t[0]])
                    #remove triangle from triangle list
                    triangles.remove(t)

            #delete all duplicate edges from the edge buffer
            #this leaves the edges of the enclosing polygon only
            edges = removeDuplicates(edges)

            #add to the triangle list all triangles formed between the point
            #and the edges of the enclosing polygon (from the edge buffer
            for j in range(len(edges)):
                v1 = edges[j][0]
                v2 = edges[j][1]
                v3 = i
                triangles.append([v1,v2,v3])

            #update progress window
            if cmds.progressWindow( query=True, isCancelled=True ) : break
            cmds.progressWindow( edit=True, step=1, status=('Points left: %d' % (self.numPoints-i)) )

        #end loop for vertices

        # FINAL STEP
        # now draw the triangles defined in the triangels list

        for t in triangles:
            print(t)
            #check if this triangle does not belong to the supertriangle,
            #if it does, jump
            if t[0] > self.numPoints-1 or t[1] > self.numPoints-1 or t[2] > self.numPoints-1: continue
            #get coordinates of the triangle t
            v1 = vertex[t[0]]
            v2 = vertex[t[1]]
            v3 = vertex[t[2]]
            #see if all coordinates contain the Z value, if not, add z=0
            if len(v1)==2: v1.append(0)
            if len(v2)==2: v2.append(0)
            if len(v3)==2: v3.append(0)
            #draw the curve
            crv = cmds.curve(p=[v1,v2,v3], d=1)
            crv = cmds.closeCurve(crv, rpo=1)
            #if outType is specified as "faces", draw the face
            if outType == "faces": cmds.planarSrf(crv)
            #to see in real time, uncomment the line below (increase operation time by circa 5 times)
            #cmds.refresh(cv=1)

        #end progress window
        cmds.progressWindow(endProgress=1)

        #feedback
        print("Delaunay triangulations created successfully!")
        print(">> %d points" % self.numPoints)
        print(">> %d triangles" % len(triangles))
        #check if you want to see time consumed
        if timer:
            delta_t = datetime.datetime.now() - currTime
            print(">> Time consumed: %s" % str(delta_t))


    def drawTriangle(self, t, vertex):
        v1 = vertex[t[0]]
        v2 = vertex[t[1]]
        v3 = vertex[t[2]]
        if len(v1)==2: v1.append(0)
        if len(v2)==2: v2.append(0)
        if len(v3)==2: v3.append(0)
        crv = cmds.curve(p=[v1,v2,v3], d=1)
        crv = cmds.closeCurve(crv, rpo=1)
        cmds.refresh(cv=1)
        return crv

    def inCircle(self, point=[0,0], triangle=[[0,0],[0,0],[0,0]]):
        '''Series of calculations to check if a certain point lies inside lies inside the circumcircle
        made up by points in triangle (x1,y1) (x2,y2) (x3,y3)'''
        #adapted from Dimitrie Stefanescu's Rhinoscript version

        #Return TRUE if the point (xp,yp)
        #The circumcircle centre is returned in (xc,yc) and the radius r
        #NOTE: A point on the edge is inside the circumcircle
        xp = point[0]
        yp = point[1]
        x1 = triangle[0][0]
        y1 = triangle[0][1]
        x2 = triangle[1][0]
        y2 = triangle[1][1]
        x3 = triangle[2][0]
        y3 = triangle[2][1]
        eps = 0.0001

        if math.fabs(y1-y2) < eps and math.fabs(y2-y3) < eps: return False

        if math.fabs(y2-y1) < eps:
            m2 = -(x3 - x2) / (y3 - y2)
            mx2 = (x2 + x3) / 2
            my2 = (y2 + y3) / 2
            xc = (x2 + x1) / 2
            yc = m2 * (xc - mx2) + my2
        elif math.fabs(y3-y2) < eps:
            m1 = -(x2 - x1) / (y2 - y1)
            mx1 = (x1 + x2) / 2
            my1 = (y1 + y2) / 2
            xc = (x3 + x2) / 2
            yc = m1 * (xc - mx1) + my1
        else:
            m1 = -(x2 - x1) / (y2 - y1)
            m2 = -(x3 - x2) / (y3 - y2)
            mx1 = (x1 + x2) / 2
            mx2 = (x2 + x3) / 2
            my1 = (y1 + y2) / 2
            my2 = (y2 + y3) / 2
            xc = (m1 * mx1 - m2 * mx2 + my2 - my1) / (m1 - m2)
            yc = m1 * (xc - mx1) + my1
        #end if
        dx = x2 - xc
        dy = y2 - yc
        rsqr = dx * dx + dy * dy
        r = math.sqrt(rsqr)
        dx = xp - xc
        dy = yp - yc
        drsqr = dx * dx + dy * dy

        if drsqr <= rsqr:
            return True
        else:
            return False

    def showAllNumbers(self):
        "Method to apply number on each vertex (for debugging only...)"
        for i in range(self.numPoints):
            txt = cmds.textCurves(text=str(i))
            cmds.scale(.5,.5,.5)
            cmds.move(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2], txt)


########################## AUXILIARY FUNCTIONS
#### vector math functions
def CrossProduct(a, b):
    "Returns the cross product between 2 vectors a and b"
    x = (a[1] * b[2]) - (a[2] * b[1])
    y = -((a[2] * b[0]) - (a[0] * b[2]))
    z = (a[0] * b[1]) - (a[1] * b[0])
    return [x, y, z]

def sum(a, b):
    "Returns the sum of vector a + b"
    x = a[0]+b[0]
    y = a[1]+b[1]
    z = a[2]+b[2]
    return [x,y,z]

def magnitude(a):
    "Returns the magnitude of vector a"
    #start and end must be lists xyz
    mag = mm.eval("mag <<%f, %f, %f >>;" % ( a[0], a[1], a[2] ))
    return mag
def distance(start, end):
    #start and end must be lists xyz
    v = [start[0]-end[0], start[1]-end[1], start[2]-end[2]] #list format x,y,z
    vector = "<<" + str(v[0]) + "," + str(v[1]) + "," + str(v[2]) + ">>"
    mag = mm.eval("mag " + vector + ";")

    return mag
def midPoint(a,b):
    "Returns the mid point between point a and b"
    mp = [ (a[0] + b[0])/2, (a[1] + b[1])/2, (a[2] + b[2])/2  ]
    return mp

def direction(a,b):
    "Returns the direction vector going from a to b"
    # Calculate direction vector
    dir = [  a[0] - b[0], a[1] - b[1], a[2] - b[2] ]  #  a-b
    return dir

def unit(a):
    "Returns the unit vector of vector a"
    aMag = magnitude(a)
    u = [  a[0]/aMag, a[1]/aMag, a[2]/aMag  ]
    return u

def multiply(a, value):
    "Return the product of vector a * value"
    prod = [ a[0]*value, a[1]*value, a[2]*value ]
    return prod

def IsBounded(item):
    for x in item:
        if x < 0:
            return False
    return True

def GetPlaneEquation(v1, v2, v3):
    x1, y1, z1 = v1[0], v1[1], v1[2]
    x2, y2, z2 = v2[0], v2[1], v2[2]
    x3, y3, z3 = v3[0], v3[1], v3[2]
    A = y1 * (z2 - z3) + y2 * (z3 - z1) + y3 * (z1 - z2)
    B = z1 * (x2 - x3) + z2 * (x3 - x1) + z3 * (x1 - x2)
    C = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    D = -(x1 * (y2 * z3 - y3 * z2) + \
        x2 * (y3 * z1 - y1 * z3) + \
        x3 * (y1 * z2 - y2 * z1))
    return [A, B, C, D]

def centerOfFace(facet):
    #find the vertices that define that face.
    vertex = cmds.polyListComponentConversion(facet, ff=1, tv=1)
    vertexFlat = cmds.ls(vertex, fl=1)
    vertCount = len(vertexFlat)
    #for each vertex go through and find it's world space position.
    vertPositionSumX = 0.
    vertPositionSumY = 0.
    vertPositionSumZ = 0.
    for v in vertexFlat:
        coordinate = cmds.pointPosition(v, w=1)
        vertPositionSumX += coordinate[0]
        vertPositionSumY += coordinate[1]
        vertPositionSumZ += coordinate[2]

    centroidX = vertPositionSumX/float(vertCount)
    centroidY = vertPositionSumY/float(vertCount)
    centroidZ = vertPositionSumZ/float(vertCount)

    return [centroidX, centroidY, centroidZ]

def faceNormal(face):
    cmds.select(face, r=1)
    pin = cmds.polyInfo(fn=1)
    tokens = pin[0].split()
    numTokens = len(tokens)
    #Make sure were looking at polyInfo data:
    if ( ( numTokens > 3 ) and ( tokens[0] == "FACE_NORMAL" ) ):
        # Maya performs data-type conversion here.
        x = (tokens[numTokens-3]);
        y = (tokens[numTokens-2]);
        z = (tokens[numTokens-1]);

        normal = "<< "+str(x)+", "+str(y)+", "+str(z)+" >>";
        #normal = [x,y,z]
        #print "normal " + str(normal)
        # Normalize it.
        normal = mm.eval("unit "+ normal+";")

    # Return it.
    return normal

def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u


def removeDuplicates(a):
    "Gets a list of lists and removes the duplicates"
    #first sort the sublists
    a = [sorted(i) for i in a]
    b = []
    for i in a:
        times = 0
        for j in a:
            if i==j: times +=1
        if times == 1: b.append(i)
    return b
#############################################

# -*- coding: utf-8 -*-
"""
https://github.com/wandth/mayaMazeGenerate/blob/master/MazeGenerate.py
加入自己的改良
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-05 11:21:25'


import maya.cmds as cmds
import pymel.core as pm
import random

# NOTE 生成迷宫阵列
row = 20
column = 20
size = 2.5
mazeComplete = False
maze = [[ [0] * 6 for r in range(row)] for c in range(column)]

for r in range(0,row):
    for c in range(0,column):
        pm.polyCube(w = 4, d = 1, h = 4, n = "Floor_%s_%s" %(r, c))
        pm.move("Floor_%s_%s" %(r, c), [r * size, -size/2, c * size])
        pm.rotate("Floor_%s_%s" %(r, c), oa = [90, 90, 0])
        maze[r][c][0] = "Floor_%s_%s" %(r, c)

        # NOTE 构建边缘
        if c == 0:
            pm.polyCube(w = 4, d = 1, h = 4, n = "WestWall_%s_%s" %(r, c))
            pm.move("WestWall_%s_%s" %(r, c), [r * size, 0, -size/2 + c * size])
            maze[r][c][1] = "WestWall_%s_%s" %(r, c)

        pm.polyCube(w = 4, d = 1, h = 4, n = "EastWall_%s_%s" %(r, c))
        pm.move("EastWall_%s_%s" %(r, c), [r * size, 0, size/2 + c * size])
        maze[r][c][2] = "EastWall_%s_%s" %(r, c)

        if r == 0:
            pm.polyCube(w = 4, d = 1, h = 4, n = "NorthWall_%s_%s" %(r, c))
            pm.move("NorthWall_%s_%s" %(r, c), [r * size -size/2, 0, c * size])
            pm.rotate("NorthWall_%s_%s" %(r, c), oa = [0, 90, 0])
            maze[r][c][3] = "NorthWall_%s_%s" %(r, c)

        pm.polyCube(w = 4, d = 1, h = 4, n = "SouthWall_%s_%s" %(r, c))
        pm.move("SouthWall_%s_%s" %(r, c), [r * size + size/2, 0, c * size])
        pm.rotate("SouthWall_%s_%s" %(r, c), oa = [0, 90, 0])
        maze[r][c][4] = "SouthWall_%s_%s" %(r, c)
        # cmds.refresh()

currentRow = 0
currentCloumn = 0
maze[currentRow][currentCloumn][5] = True

# NOTE 生成迷宫阵列
def objIsExistsAndEdlete(_cellName):
    if cmds.objExists(_cellName):
        pm.delete(_cellName)
        cmds.refresh()
        
def routeAvailabe(_row, _column):
    availabeRoutes = 0
    if _row > 0 and not maze[_row - 1][_column][5]:
        availabeRoutes += 1
        
    if _row < row - 1 and not maze[_row + 1][_column][5]:
        availabeRoutes += 1

    if _column > 0 and not maze[_row][_column - 1][5]:
        availabeRoutes += 1

    if _column < column - 1 and not maze[_row][_column + 1][5]:
        availabeRoutes += 1
        
    if availabeRoutes > 0:
        return True
    else:
        return False

    
def cellAvailable(_row, _column):
    if _row >= 0 and _row < row and _column >= 0 and _column < column and not maze[_row][_column][5]:
        return True
    else:
        return False

def kills():
    global currentCloumn
    global currentRow
    
    while routeAvailabe(currentRow, currentCloumn):
        direction = random.randint(1, 5)
        
        if direction == 1 and cellAvailable(currentRow - 1, currentCloumn):
            objIsExistsAndEdlete("NorthWall_%s_%s" %(currentRow, currentCloumn))
            objIsExistsAndEdlete("SouthWall_%s_%s" %(currentRow - 1, currentCloumn))
            currentRow -= 1

        if direction == 2 and cellAvailable(currentRow + 1, currentCloumn):
            objIsExistsAndEdlete("SouthWall_%s_%s" %(currentRow, currentCloumn))
            objIsExistsAndEdlete("NorthWall_%s_%s" %(currentRow + 1, currentCloumn))
            currentRow += 1

        if direction == 3 and cellAvailable(currentRow, currentCloumn + 1):
            objIsExistsAndEdlete("EastWall_%s_%s" %(currentRow, currentCloumn))
            objIsExistsAndEdlete("WestWall_%s_%s" %(currentRow, currentCloumn + 1))
            currentCloumn += 1
            
        if direction == 4 and cellAvailable(currentRow, currentCloumn - 1):
            objIsExistsAndEdlete("WestWall_%s_%s" %(currentRow, currentCloumn))
            objIsExistsAndEdlete("EastWall_%s_%s" %(currentRow, currentCloumn - 1))
            currentCloumn -= 1
            
        maze[currentRow][currentCloumn][5] = True


                
def destoryAdjacentWall(_row, _column):
    wallDestoryed = False
    while not wallDestoryed:
        direction = random.randint(1, 5)
        if direction == 1 and _row > 0 and maze[_row - 1][ _column][5]:
            objIsExistsAndEdlete("NorthWall_%s_%s" %(_row, _column))
            objIsExistsAndEdlete("SouthWall_%s_%s" %(_row - 1, _column))
            wallDestoryed = True
        elif direction == 2 and _row < row - 2 and maze[_row + 1][ _column][5]:
            objIsExistsAndEdlete("SouthWall_%s_%s" %(_row, _column))
            objIsExistsAndEdlete("NorthWall_%s_%s" %(_row + 1, _column))
            wallDestoryed = True

        elif direction == 3 and _column > 0 and maze[_row][ _column - 1][5]:
            objIsExistsAndEdlete("EastWall_%s_%s" %(_row, _column))
            objIsExistsAndEdlete("WestWall_%s_%s" %(_row, _column - 1))
            wallDestoryed = True
            
        elif direction == 4 and _column < column - 2 and maze[_row][ _column + 1][5]:
            objIsExistsAndEdlete("WestWall_%s_%s" %(_row, _column))
            objIsExistsAndEdlete("EastWall_%s_%s" %(_row - 1, _column + 1))
            wallDestoryed = True

def cellHasAnAdjacentVisitedCell(_row, _column):
    visitedCell = 0
    if _row > 0 and maze[_row - 1][_column][5]:
        visitedCell +=1
    if _row < row - 2 and maze[_row + 1][_column][5]:
        visitedCell +=1

    if _column > 0 and maze[_row][_column - 1][5]:
        visitedCell +=1
    if _column < column - 2 and maze[_row][_column + 1][5]:
        visitedCell +=1
    
    if visitedCell > 0:
        return True
    else:
        return False


def hunts():
    global mazeComplete
    mazeComplete = True
    
    for r in range(row):
        for c in range(column):
            if not maze[r][c][5] and cellHasAnAdjacentVisitedCell(r, c):
                mazeComplete = False
                currentRow = r
                currentCloumn = c
                destoryAdjacentWall(currentRow, currentCloumn)
                maze[currentRow][currentCloumn][5] = True
                
                return     

        
        
while not mazeComplete:
    kills()
    hunts()

# for i in range(100):
    # kills()
    # hunts()




import pymel.core as pm
import pymel.core.datatypes as dt

L,R = pm.ls(sl=1)

L = dt.Vector(L.getRotation(space="world"))
R = dt.Vector(R.getRotation(space="world"))

print L
print R
print L-R

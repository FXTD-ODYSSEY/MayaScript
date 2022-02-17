from maya import OpenMaya
import cloudpickle
mesh = OpenMaya.MFnMesh()
print(mesh)

class Mesh():
    pass

mesh = Mesh()
path = r"F:\repo\MayaScript\_msic\py\cloudpickle\data"
with open(path, 'w') as f:
    cloudpickle.dump(mesh,f)

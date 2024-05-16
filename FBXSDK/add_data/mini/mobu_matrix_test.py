import pyfbsdk as mobu
from PySide import QtCore

# TODO 获取 RightFoot

# myCube = mobu.FBModelCube("cube")
# myCube.Show = True
# myCube.Translation = mobu.FBVector3d(222, 45, 45)
# myCube.Rotation = mobu.FBVector3d(222, 45, 45)
# matrix = mobu.FBMatrix()
# myCube.GetMatrix(matrix)
# print(matrix)

# (0.500000, 0.500000, -0.707107, 0.000000)
# (0.190917, -0.860048, -0.473147, 0.000000)
# (-0.844719, 0.101574, -0.525483, 0.000000)
# (222.000000, 45.000000, 45.000000, 1.000000)

# lModelList = mobu.FBModelList()

# # Get list of selected models in scene graph order
# mobu.FBGetSelectedModels( lModelList)

# print()

fbx_path = r"D:\lumi\lumi_project\lumi_project_develop\Art\Assets\Actor\Daodao02\DaodaoFlat\Rigging\Live_Rig\Rig\Actor_Daodao02_DaodaoFlat_Mocap_Rig.fbx"

app = mobu.FBApplication()
app.FileOpen(fbx_path)
mobu.FBSystem().Renderer.Render()
# def get_matrix():
foot_joint = mobu.FBFindModelByLabelName("RightFoot")
print(foot_joint)
matrix = mobu.FBMatrix()
foot_joint.GetMatrix(matrix, mobu.FBModelTransformationType.kModelTransformation, True)
print(matrix)

# QtCore.QTimer.singleShot(0,get_matrix)

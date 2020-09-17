from maya import cmds
from maya import mel

cmds.file(new=1,f=1)

path = r"D:\_minigame\ShadowTacitcs\gameplay (19)\gameplay.fbx"
path = path.replace('\\', '/')
mel.eval('''
FBXImport -f "%s"
'''% path)

cmds.delete(cmds.ls('*Occluder*'))
cmds.delete(cmds.ls('*occluder*'))
# cmds.delete(cmds.ls('*collider*'))
# cmds.delete(cmds.ls('*tv_*'))
# cmds.delete(cmds.ls('*TV_*'))
# cmds.delete(cmds.ls('*triggervol*'))

mel.eval('''
modelEditor -e -allObjects 0 modelPanel4;
modelEditor -e -polymeshes true modelPanel4;
modelPanelBarShadingCallback("TexturedBtn", "MainPane|viewPanes|modelPanel4|modelPanel4|modelEditorTabLayout|modelPanel4", "MainPane|viewPanes|modelPanel4|modelPanel4|modelEditorIconBar"); 
''')
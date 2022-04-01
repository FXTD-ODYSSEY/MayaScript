import hou
path = r'C:\Users\timmyliang\Documents\houdini19.0\packages\SOP_vellumconstraints.png'
icon = hou.qt.Icon('SOP_vellumconstraints')
pixmap = icon.pixmap(2048,2048)
pixmap.save(path)

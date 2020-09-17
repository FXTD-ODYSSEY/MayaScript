for i,mesh in enumerate(cmds.ls(type="mesh",l=1)):
    try:
            
        if not cmds.listConnections(mesh,type="shadingEngine"):
            cmds.delete(cmds.listRelatives(mesh,p=1))
    except:
        cmds.delete(mesh)
        print(mesh)
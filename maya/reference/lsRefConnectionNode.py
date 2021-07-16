for i,ref in enumerate(cmds.ls(references=1)):
    for conn in cmds.listConnections(ref):
        conn_type = cmds.objectType(conn)

        for text in ['animcurve','reference','pairblend','constraint','fosterparent']:
            if text in conn_type.lower():
                break
        else:
            print conn


    

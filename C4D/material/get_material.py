import c4d
import os
from pprint import pprint

c4d.CallCommand(13957) # Clear Console
doc = c4d.documents.GetActiveDocument()

############################################################
# recursive function where we do stuff to the shaders
############################################################
def shadertree(shader):
    # Loop through the BaseList
    while(shader):
        print(shader)
        # This is where you do stuff
        # If it's a bitmap, we'll look at the filename
        if shader.GetType() == c4d.Xbitmap:
            filename = shader[c4d.BITMAPSHADER_FILENAME]
            print (filename)
            # for instance we can set the filename to just the file part
            # filename = os.path.basename(filename)
            # shader[c4d.BITMAPSHADER_FILENAME] = filename
         
        # Check for child shaders & recurse
        if shader.GetDown(): shadertree(shader.GetDown())
        # Get the Next Shader
        shader = shader.GetNext()
         
############################################################
# main function
############################################################

def iterate_objects(objects=None):
    ret_list = []
    for obj in objects or doc.GetObjects():
        # yield obj
        print(obj.GetChildren())
        # ret_list.append(obj)
        ret_list.extend(iterate_objects(obj.GetChildren()))
    return ret_list

def main():
    # obj = doc.GetFirstMaterial()
    # print(mat)
    # pprint(dir(mat))
    # print(mat.GetNodeMaterialReference ())
    # return

    # inst = op.GetDataInstance()
    for obj in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        print(obj.GetName())
        tag = obj.GetTag(c4d.Ttexture)
        if not tag:
            continue

        material = tag.GetMaterial()
        print(material)
        shader = material.GetFirstShader()
        shadertree(shader)
        # print(material)
        # print(shader)
        # if shader and shader.GetType() == c4d.Xbitmap:
        #     filename = shader[c4d.BITMAPSHADER_FILENAME]
        #     print (obj,filename)
        # print(obj,material)
        
    # material = tag.GetMaterial()
 
if __name__=='__main__':
    main()
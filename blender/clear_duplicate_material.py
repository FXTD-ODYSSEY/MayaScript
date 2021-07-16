import bpy
import hashlib

# NOTE 遍历所有的材质
material_dict = {}
for obj in bpy.context.selectable_objects:
    replace_material = {}
    for slot in obj.material_slots:
        material = slot.material
        matnodes = material.node_tree.nodes

        m = hashlib.md5()
        for tex_node in matnodes:
            if isinstance(tex_node, bpy.types.ShaderNodeTexImage):
                path = tex_node.image.filepath.encode()
                m.update(path)

        md5 = m.hexdigest()
        if md5 not in material_dict:
            material_dict[md5] = material
        else:
            # NOTE 删除材质
            bpy.data.materials.remove(material)
            # NOTE 替换为 md5 一致
            slot.material = material_dict[md5]
            
    
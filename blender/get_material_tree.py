import bpy

for obj in bpy.context.selected_objects:
    for slot in obj.material_slots:
        material = slot.material
        matnodes = material.node_tree.nodes
        for node in matnodes:
            print(node)
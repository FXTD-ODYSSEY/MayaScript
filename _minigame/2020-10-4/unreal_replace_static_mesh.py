import unreal

actors = unreal.EditorLevelLibrary.get_all_level_actors()
for actor in actors:
    if not isinstance(actor,unreal.StaticMeshActor):
        continue
    comp = actor.static_mesh_component
    mesh = comp.static_mesh 
    path = mesh.get_path_name()
    if path.startswith("/Game/Japanese_Temple/"):
        path = path.replace("/Game/Japanese_Temple/","/Game/改Japanese_Temple/")
        comp.set_editor_property("static_mesh",unreal.load_asset(path))
    
    material_list = []
    print(comp.get_editor_property("override_materials"))
    for material in comp.get_editor_property("override_materials"):
        print(unicode(actor))
        path = material.get_path_name()
        path = path.replace("/Game/Japanese_Temple/","/Game/改Japanese_Temple/")
        material_list.append(unreal.load_asset(path))
    
    if material_list:
        comp.set_editor_property("override_materials",material_list)
    
        
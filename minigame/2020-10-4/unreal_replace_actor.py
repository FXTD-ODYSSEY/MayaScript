import unreal

import os
from collections import defaultdict


# actors = unreal.EditorLevelLibrary.get_all_level_actors()
# for actor in actors:
#     if isinstance(actor,unreal.StaticMeshActor):
#         comp = actor.static_mesh_component
#         mesh = comp.static_mesh 
#         path = mesh.get_path_name()
#         if path.startswith("/Game/Japanese_Temple/"):
#             path = path.replace("/Game/Japanese_Temple/","/Game/改Japanese_Temple/")
#             comp.set_editor_property("static_mesh",unreal.load_asset(path))
#     elif isinstance(actor.get_class(),unreal.BlueprintGeneratedClass):
#         pass

BP_dict = defaultdict(list)
actors = unreal.EditorLevelLibrary.get_all_level_actors()
# actors = unreal.EditorLevelLibrary.get_selected_level_actors()
for actor in actors:
    actor_cls = actor.get_class()
    if not isinstance(actor_cls,unreal.BlueprintGeneratedClass):
        continue
    path = actor_cls.get_path_name()
    if path.startswith("/Game/Japanese_Temple/"):
        BP_dict[path].append(actor)

for path,actors in BP_dict.items():
    path = path.replace("/Game/Japanese_Temple/","/Game/改Japanese_Temple/")
    gen_cls =unreal.load_object(None,path)
    unreal.EditorLevelLibrary.convert_actors(actors,gen_cls,os.path.dirname(path))

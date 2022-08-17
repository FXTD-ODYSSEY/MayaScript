import unreal

for asset in unreal.EditorUtilityLibrary.get_selected_assets():
    if not isinstance(asset,unreal.GroomAsset):
        continue
    data =asset.get_editor_property("asset_user_data") 
    print(data)
    pass
        


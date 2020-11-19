import unreal

asset_lib = unreal.EditorAssetLibrary()

for asset_path in asset_lib.list_assets(u'/Game/Japanese_Temple'):

    path = asset_path.replace(u'/Game/Japanese_Temple',u'/Game/Japanese_Temple2')
    asset = unreal.load_asset(asset_path)
    match_asset = unreal.load_asset(path)
    
    # print(asset)
    # print(match_asset)
    asset_lib.consolidate_assets(match_asset,[asset])
    # break
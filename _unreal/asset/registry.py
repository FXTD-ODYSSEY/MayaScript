
import unreal
asset_tool = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
path = '/Game/ArtResources/Characters/Roles/Actor/Sanji01/BluePrints/Actor/90065_A.90065_A'
data = asset_registry.get_asset_by_object_path(path)

print(data.is_u_asset())
print(data.is_valid())

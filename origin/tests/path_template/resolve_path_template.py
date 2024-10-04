
root = {"work": "work_directory"}
project = {"name": "project_name"}
hierarchy = "hierarchy_path"
asset = "asset_name"
family = "family_name"
subset = "subset_name"
version = "v001"
originalBasename = "basename"
frame = "001"
udim = "1001"
ext = "exr"


folder_template = f"{root['work']}/{project['name']}/{hierarchy}/{asset}/publish/{family}/{subset}/{version}"
file_template = f"{originalBasename}<.{frame}><_{udim}>.{ext}"
path_template = f"{folder_template}/{file_template}"

print("Folder: ", folder_template)
print("File: ", file_template)
print("Path: ", path_template)
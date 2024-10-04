'''
DOC EXAMPLE:

{
    "_id": "ObjectId",
    "name": "hulk",
    "type": "Character",
    "project": "projectA",
    "db_path": "assets/characters",
    "tasks": {
        "modeling": {
            "status": "In Progress",
            "versions": []
        },
        "texturing": {
            "status": "Not Started",
            "versions": []
        }
    }
}


'''
protocols = {
    "modeling": {
        "asset_type": "Geometry",
        "version_type": "GeometryAssetVersion",
        "components": ["master_scene", "usd"]
    },
    "texturing": {
        "asset_type": "Texture",
        "version_type": "TextureAssetVersion",
        "components": ["diffuse_map", "normal_map"]
    }
}

import os
from pymongo import MongoClient
from protocols import protocols


class Publisher:
    def __init__(self, project, db_path, current_asset, current_task):
        self.project = project
        self.db_path = db_path
        self.current_asset = current_asset
        self.current_task = current_task
        self.protocol = protocols.get(current_task)
        if not self.protocol:
            raise ValueError(f"No protocol defined for task type: {current_task}")

        self.client = MongoClient('localhost', 27017)
        self.db = self.client.vfx_pipeline
        self.assets_collection = self.db.assets
        self.versions_collection = self.db.versions
        self.components_collection = self.db.components

    def publish(self):
        asset = self._get_asset()
        if not asset:
            raise ValueError(f"Asset '{self.current_asset}' not found.")

        version = self._create_version(asset)
        self._create_components(version)
        self._update_task_status(asset, "Published")

    def _get_asset(self):
        return self.assets_collection.find_one({"name": self.current_asset, "project": self.project})

    def _create_version(self, asset):
        task_info = asset["tasks"].get(self.current_task)
        if not task_info:
            raise ValueError(f"Task '{self.current_task}' not found in asset '{self.current_asset}'.")

        version_number = len(task_info["versions"]) + 1
        version_name = f"{self.current_asset}_{self.current_task}_publish_v{version_number:04d}"
        version = {
            "name": version_name,
            "type": self.protocol["version_type"],
            "asset_id": asset["_id"],
            "task_type": self.current_task,
            "status": "In Progress",
            "components": []
        }
        version_id = self.versions_collection.insert_one(version).inserted_id
        version["_id"] = version_id
        self.assets_collection.update_one(
            {"_id": asset["_id"]},
            {"$push": {f"tasks.{self.current_task}.versions": version_id}}
        )
        return version

    def _create_components(self, version):
        for component_name in self.protocol["components"]:
            file_path = self._generate_file_path(component_name)
            component = {
                "name": component_name,
                "type": component_name + "Component",
                "version_id": version["_id"],
                "file_path": file_path,
                "status": "Ready"
            }
            self.components_collection.insert_one(component)
            self.versions_collection.update_one(
                {"_id": version["_id"]},
                {"$push": {"components": component}}
            )

    def _generate_file_path(self, component_name):
        base_path = f"{self.db_path}/{self.current_asset}"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        file_path = f"{base_path}/{component_name}.file_ext"  # Adjust file extension based on component type
        # Here you would implement the logic to export the file from Maya, etc.
        return file_path

    def _update_task_status(self, asset, new_status):
        self.assets_collection.update_one(
            {"_id": asset["_id"]},
            {"$set": {f"tasks.{self.current_task}.status": new_status}}
        )


import maya.cmds as cmds


class MayaPublisher(Publisher):
    def _generate_file_path(self, component_name):
        base_path = f"{self.db_path}/{self.current_asset}"
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if component_name == "master_scene":
            file_path = f"{base_path}/{component_name}.ma"
            cmds.file(rename=file_path)
            cmds.file(save=True, type='mayaAscii')
        elif component_name == "usd":
            file_path = f"{base_path}/{component_name}.usd"
            # Example command to export USD from Maya
            cmds.mayaUSDExport(file=file_path, selection=True)
        else:
            file_path = f"{base_path}/{component_name}.ext"  # Replace with appropriate extension and export logic
        return file_path


def main():
    project = "projectA"
    db_path = "assets/characters"
    current_asset = "hulk"
    current_task = "modeling"

    publisher = MayaPublisher(project, db_path, current_asset, current_task)
    publisher.publish()

if __name__ == "__main__":
    main()
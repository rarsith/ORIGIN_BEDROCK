from typing import Optional, List, Type
import dataclasses
from PySide2 import QtWidgets
from pymongo import MongoClient  # Assuming you use pymongo for MongoDB interactions


# Example of a MongoDB service for separation of concerns
class MongoService:
    def __init__(self, client: MongoClient):
        self.db = client["vfx_pipeline"]

    def find_by_key(self, key: str, value: str):
        return self.db["entities"].find_one({key: value})

    def find_children(self, parent_id: str):
        return self.db["entities"].find({"parent": parent_id})

    def find_tasks(self, parent_id: str):
        return self.db["entities"].find({"parent": parent_id, "type": "task"})


mongo_service = MongoService(MongoClient())  # Replace with actual MongoDB client


def get_type_class(entity_data) -> Type["Entity"]:
    if entity_data["type"] == "project":
        return Project
    elif entity_data["type"] == "shot":
        return Shot
    elif entity_data["type"] == "sequence":
        return Sequence
    elif entity_data["type"] == "group":
        return Group
    else:
        raise ValueError(f"Unsupported entity type: {entity_data['type']}")


@dataclasses.dataclass
class Entity:
    name: str
    id: str
    type: str

    parent: Optional["Entity"] = None
    children: List["Entity"] = dataclasses.field(default_factory=list)

    def get_parent(self) -> Optional["Entity"]:
        parent_id = self.id.rsplit(".", 1)[0]
        entity_data = mongo_service.find_by_key("id", parent_id)

        if not entity_data:
            return None

        base_class = get_type_class(entity_data)
        return base_class(**entity_data)

    def get_children(self) -> List["Entity"]:
        children_data = mongo_service.find_children(self.id)
        return [get_type_class(child)(**child) for child in children_data]

    def get_tasks(self):
        tasks = list(mongo_service.find_tasks(self.id))
        for child in self.get_children():
            tasks += child.get_tasks()
        return tasks


@dataclasses.dataclass
class Project(Entity):
    show_type: str = ""  # Example additional field


@dataclasses.dataclass
class Sequence(Entity):
    pass


@dataclasses.dataclass
class Shot(Entity):
    def get_sequence(self) -> Sequence:
        possible_sequence_ids = []
        parent_id = self.id.rsplit(".", 1)[0]
        while "." in parent_id:
            possible_sequence_ids.append(parent_id)
            parent_id = parent_id.rsplit(".", 1)[0]

        sequence_data = mongo_service.find_by_key(
            "id", {"$in": possible_sequence_ids, "type": "sequence"}
        )
        if sequence_data:
            return Sequence(**sequence_data)
        return None


@dataclasses.dataclass
class Group(Entity):
    pass


class MyDisplayWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._context = None

        layout = QtWidgets.QVBoxLayout(self)
        self.name_display = MyNameDisplayWidget(self)
        self.type_display = MyTypeDisplayWidget(self)
        layout.addWidget(self.name_display)
        layout.addWidget(self.type_display)

    def set_context(self, context: Entity):
        self.name_display.set_context(context)
        self.type_display.set_context(context)
        self._context = context

    def get_context(self):
        return self._context


class MyNameDisplayWidget(QtWidgets.QLabel):
    def set_context(self, context: Entity):
        self.setText(context.name if context else "")


class MyTypeDisplayWidget(QtWidgets.QLabel):
    def set_context(self, context: Entity):
        self.setText(context.type if context else "")


# Example usage:
qapp = QtWidgets.QApplication([])
widget = MyDisplayWidget()

project = Project(name="Sample Project", id="project1", type="project")
widget.set_context(project)

print("Selected context:", widget.get_context())

widget.show()
qapp.exec_()

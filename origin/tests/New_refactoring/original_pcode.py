import dataclasses
from typing import Optional, List, Type

from Qt import QtWidgets


def get_type_class(entity_data) -> Type["Entity"]:
    if entity_data["type"] == "project":
        return Project
    elif entity_data["type"] == "shot":
        return Shot


@dataclasses.dataclass
class Entity:
    name: str
    id: str
    type: str

    parent: Optional["Entity"]
    children: List["Entity"]

    def get_parent(self) -> Optional["Entity"]:
        parent_id = self.id.rsplit(".", 1)[0]
        entity_data = mongo.find_by_key("id", parent_id)

        if not entity_data:
            return None

        base_class = get_type_class(entity_data)
        return base_class(**entity_data)

    def set_parent(self, parent):
        pass

    def get_children(self) -> List["Entity"]:
        children_data = mongo.find_by_key("parent", self.id)
        children = []
        for child_data in children_data:
            children.append(get_type_class(child_data)(**children_data))
        return children

    def get_tasks(self):

        tasks = mongo.find_by_key({"type": "task", "parent": self.id})

        for child in self.get_children():
            tasks += child.get_tasks()

        return tasks


@dataclasses.dataclass
class Project(Entity):
    show_type: str


@dataclasses.dataclass
class Sequence(Entity):
    pass


@dataclasses.dataclass
class Shot(Entity):
    def get_sequence(self) -> Sequence:
        # Example:
        # shot = "MooMoo.SQ001.myShitGroup.SH001"
        # possible_sequence_ids = [
        #     "MooMoo.SQ001.myShitGroup",
        #     "MooMoo.SQ001",
        #     "MooMoo",
        # ]

        possible_sequence_ids = []
        parent_id = self.id.rsplit(".", 1)[0]
        while "." in parent_id:
            possible_sequence_ids.append(parent_id)
            parent_id = parent_id.rsplit(".", 1)[0]

        sequence = mongo.find_by_key(
            {
                "type": "sequence",
                "parent": {"in": possible_sequence_ids},
            },
        )
        return Sequence(**sequence)


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
        if not context:
            label = ""
        else:
            label = context.name

        self.setText(label)


class MyTypeDisplayWidget(QtWidgets.QLabel):
    def set_context(self, context: Entity):
        if not context:
            label = ""
        else:
            label = context.type

        self.setText(label)


qapp = QtWidgets.QApplication([])
widget = MyDisplayWidget()

project = Project(name="whatever")
widget.set_context(project)

print("Selected", widget.get_context())

widget.show()
qapp.exec()
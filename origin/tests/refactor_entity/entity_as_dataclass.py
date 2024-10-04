from typing import Optional, List, Dict
from pydantic import BaseModel


class Entity(BaseModel):
    type: Optional[str]
    data: Optional[str]
    stack_streams: Optional[str]
    parent: Optional[str]
    visual_parent: Optional[str]
    entry_name: Optional[str]
    active: Optional[bool]
    definition: Optional[str]
    origin_db_path: Optional[str]
    tasks: Optional[dict]
    children: Optional[list]
    config: Optional[dict]
    components: Optional[dict]
    assigned_to: Optional[list]





    def __init__(self, entity_id=None, operation=None, db_operation=None, db_collection=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id
        self.db_collection = db_collection

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value is not None:
            method(value)
        else:
            return method()

    @property
    def entity_type(self):
        attribute_path = DbEntityAttrPath().to_type()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_type.setter
    def entity_type(self, ent_type):
        attribute_path = DbEntityAttrPath().to_type()
        self._create_op_inst(attribute_path=attribute_path, value=ent_type)

    @property
    def entity_data(self):
        attribute_path = DbEntityAttrPath().to_data()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_data.setter
    def entity_data(self, ent_data):
        attribute_path = DbEntityAttrPath().to_data()
        self._create_op_inst(attribute_path=attribute_path, value=ent_data)

    @property
    def stack_stream(self):
        attribute_path = DbEntityAttrPath().to_stack_stream()
        return self._create_op_inst(attribute_path=attribute_path)

    @stack_stream.setter
    def stack_stream(self, ent_data):
        attribute_path = DbEntityAttrPath().to_stack_stream()
        self._create_op_inst(attribute_path=attribute_path, value=ent_data)

    @property
    def entity_parent(self):
        attribute_path = DbEntityAttrPath().to_parent()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_parent.setter
    def entity_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_parent()
        self._create_op_inst(attribute_path=attribute_path, value=ent_parent)

    @property
    def entity_visual_parent(self):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_visual_parent.setter
    def entity_visual_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        self._create_op_inst(attribute_path=attribute_path, value=ent_parent)

    @property
    def entity_name(self):
        attribute_path = DbEntityAttrPath().to_entity_name()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_name.setter
    def entity_name(self, ent_name):
        attribute_path = DbEntityAttrPath().to_entity_name()
        self._create_op_inst(attribute_path=attribute_path, value=ent_name)

    @property
    def is_active(self):
        attribute_path = DbEntityAttrPath().to_is_active()
        return self._create_op_inst(attribute_path=attribute_path)

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbEntityAttrPath().to_is_active()
        self._create_op_inst(attribute_path=attribute_path, value=set_is_active)

    @property
    def definition(self):
        attribute_path = DbEntityAttrPath().to_definition()
        return self._create_op_inst(attribute_path=attribute_path)

    @definition.setter
    def definition(self, set_definition):
        attribute_path = DbEntityAttrPath().to_definition()
        self._create_op_inst(attribute_path=attribute_path, value=set_definition)

    @property
    def origin_db_path(self):
        attribute_path = DbEntityAttrPath().to_origin_db_path()
        return self._create_op_inst(attribute_path=attribute_path)

    @origin_db_path.setter
    def origin_db_path(self, set_origin_db_path):
        attribute_path = DbEntityAttrPath().to_origin_db_path()
        self._create_op_inst(attribute_path=attribute_path, value=set_origin_db_path)

    @property
    def children(self):
        attribute_path = DbEntityAttrPath().to_children()
        return self._create_op_inst(attribute_path=attribute_path)

    @children.setter
    def children(self, set_children):
        attribute_path = DbEntityAttrPath().to_children()
        self._create_op_inst(attribute_path=attribute_path, value=set_children)

    def all_tasks(self):
        return Tasks(operation=self.operation, db_operation=self.db_operation)

    @property
    def tasks(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        return self._create_op_inst(attribute_path=attribute_path)

    @tasks.setter
    def tasks(self, set_tasks):
        attribute_path = DbEntityAttrPath().to_tasks()
        self._create_op_inst(attribute_path=attribute_path, value=set_tasks)

    @property
    def config(self):
        attribute_path = DbEntityAttrPath().to_config()
        return self._create_op_inst(attribute_path=attribute_path)

    @config.setter
    def config(self, set_config):
        attribute_path = DbEntityAttrPath().to_config()
        self._create_op_inst(attribute_path=attribute_path, value=set_config)

    @property
    def components(self):
        attribute_path = DbEntityAttrPath().to_components()
        return self._create_op_inst(attribute_path=attribute_path)

    @components.setter
    def components(self, set_components):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        self._create_op_inst(attribute_path=attribute_path, value=set_components)

    @property
    def assigned_to(self):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        return self._create_op_inst(attribute_path=attribute_path)

    @assigned_to.setter
    def assigned_to(self, set_assigned_to):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        self._create_op_inst(attribute_path=attribute_path, value=set_assigned_to)

from o_database.mongo_connection import MongoConnection
from envars.origin_envars import OriginEnvar
from o_database.collections.connections import ProjectCollections
from o_database.collections.pipelines import OriginDBPipelines
from o_database.entities.attributes_paths import DbEntityAttrPath, DbTaskAttrPath, DbPubSlotsAttrPath, DbProjectAttrPath
from o_database.entities.ids import DbIds
from o_database.collections.operators import FindInCollection


class Entity:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()

    @property
    def entity_type(self):
        attribute_path = DbEntityAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()
        return results

    @entity_type.setter
    def entity_type(self, ent_type):
        attribute_path = DbEntityAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_type)

    @property
    def entity_data(self):
        attribute_path = DbEntityAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_data.setter
    def entity_data(self, ent_data):
        attribute_path = DbEntityAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_data)

    @property
    def entity_parent(self):
        attribute_path = DbEntityAttrPath().to_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_parent.setter
    def entity_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_parent)

    @property
    def entity_visual_parent(self):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_visual_parent.setter
    def entity_visual_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_parent)

    @property
    def entity_name(self):
        return

    @entity_name.setter
    def entity_name(self, ent_name):
        pass

    @property
    def is_active(self):
        attribute_path = DbEntityAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbEntityAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_is_active)

    @property
    def definition(self):
        attribute_path = DbEntityAttrPath().to_definition()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @definition.setter
    def definition(self, set_definition):
        attribute_path = DbEntityAttrPath().to_definition()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_definition)

    @property
    def origin_db_path(self):
        attribute_path = DbEntityAttrPath().to_origin_db_path()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @origin_db_path.setter
    def origin_db_path(self, set_origin_db_path):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_origin_db_path)

    @property
    def children(self):
        attribute_path = DbEntityAttrPath().to_children()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @children.setter
    def children(self, set_children):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_children)

    def all_tasks(self):
        return Tasks(operation=self.operation, db_operation=self.db_operation)

    @property
    def tasks(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @tasks.setter
    def tasks(self, set_tasks):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_tasks)

    @property
    def config(self):
        attribute_path = DbEntityAttrPath().to_config()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @config.setter
    def config(self, set_config):
        attribute_path = DbEntityAttrPath().to_config()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_config)

    @property
    def components(self):
        attribute_path = DbEntityAttrPath().to_components()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @components.setter
    def components(self, set_components):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_components)

    @property
    def assigned_to(self):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @assigned_to.setter
    def assigned_to(self, set_assigned_to):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_assigned_to)

class EntityById:
    def __init__(self, operation=None, db_operation=None, entity_id=None):
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = entity_id


    @property
    def entity_type(self):
        attribute_path = DbEntityAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()
        return results

    @entity_type.setter
    def entity_type(self, ent_type):
        attribute_path = DbEntityAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_type)

    @property
    def entity_data(self):
        attribute_path = DbEntityAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_data.setter
    def entity_data(self, ent_data):
        attribute_path = DbEntityAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_data)

    @property
    def entity_parent(self):
        attribute_path = DbEntityAttrPath().to_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_parent.setter
    def entity_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_parent)

    @property
    def entity_visual_parent(self):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @entity_visual_parent.setter
    def entity_visual_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(ent_parent)

    @property
    def entity_name(self):
        return

    @entity_name.setter
    def entity_name(self, ent_name):
        pass

    @property
    def is_active(self):
        attribute_path = DbEntityAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbEntityAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_is_active)

    @property
    def definition(self):
        attribute_path = DbEntityAttrPath().to_definition()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @definition.setter
    def definition(self, set_definition):
        attribute_path = DbEntityAttrPath().to_definition()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_definition)

    @property
    def origin_db_path(self):
        attribute_path = DbEntityAttrPath().to_origin_db_path()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @origin_db_path.setter
    def origin_db_path(self, set_origin_db_path):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_origin_db_path)

    @property
    def children(self):
        attribute_path = DbEntityAttrPath().to_children()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @children.setter
    def children(self, set_children):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_children)

    def all_tasks(self):
        return Tasks(operation=self.operation, db_operation=self.db_operation)

    @property
    def tasks(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @tasks.setter
    def tasks(self, set_tasks):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_tasks)

    @property
    def config(self):
        attribute_path = DbEntityAttrPath().to_config()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @config.setter
    def config(self, set_config):
        attribute_path = DbEntityAttrPath().to_config()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_config)

    @property
    def components(self):
        attribute_path = DbEntityAttrPath().to_components()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @components.setter
    def components(self, set_components):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_components)

    @property
    def assigned_to(self):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @assigned_to.setter
    def assigned_to(self, set_assigned_to):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_assigned_to)


class Groups(Entity):
    def __init__(self, operation=None, db_operation=None):
        super(Groups, self).__init__()
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()


class Assets(Entity):
    def __init__(self, operation=None, db_operation=None):
        super(Assets, self).__init__()
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()


class CollectionOperators:
    def __init__(self, db_collection):
        self.db = MongoConnection().origin_production_database()
        if db_collection:
            self.db_collection = self.db[db_collection]


    def project_root_children(self):
        ppe = OriginDBPipelines()
        crit = {"origin_db_path": f"{OriginEnvar().resolve_context_to_base()}"}
        pipe = ppe.generate_pipeline(crit)

        try:
            if self.db_collection:
                result_docs = self.db_collection.aggregate(pipe)
                results = ([x for x in result_docs])
                return results
        except Exception as e:
            print(e)

    def entity_by_id(self, doc_id):
        db_document = self.db_collection.find_one({"_id": doc_id})

        return db_document

    def entity_children_ids(self, doc_id):
        db_document = self.db_collection.find_one({"_id": doc_id})

        if db_document:
            return db_document.get('visual_children', [])
        else:
            return []

    def with_statuses(self, status: list):
        pass

    def with_owners(self, user_names: list):
        pass

    def with_dates(self, input_dates: list):
        pass

    def with_tasks(self, task_names: list):
        pass

    def with_names(self, entity_names: list):
        pass

    def with_ids(self, entity_ids: list):
        pass


class Tasks:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()


    def multiple(self, ops_list):
        for operation in ops_list:
            for attr_path, attr_value in operation.items():
                method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                                entry_id=self.current_entity_id,
                                                attribute=attr_path), self.db_operation)
                method(attr_value)


    def names(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()
        return list(results.keys())

    @property
    def is_active(self):
        attribute_path = DbTaskAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @is_active.setter
    def is_active(self, set_active):
        attribute_path = DbTaskAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_active)

    @property
    def user(self):
        attribute_path = DbTaskAttrPath().to_artist()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @user.setter
    def user(self, set_user):
        attribute_path = DbTaskAttrPath().to_artist()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_user)

    @property
    def bid_days(self):
        attribute_path = DbTaskAttrPath().to_bid_days()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @bid_days.setter
    def bid_days(self, set_bid_days):
        attribute_path = DbTaskAttrPath().to_bid_days()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_bid_days)

    @property
    def end_date(self):
        attribute_path = DbTaskAttrPath().to_end_date()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @end_date.setter
    def end_date(self, set_end_date):
        attribute_path = DbTaskAttrPath().to_end_date()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_end_date)

    @property
    def milestones(self):
        attribute_path = DbTaskAttrPath().to_milestones()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @milestones.setter
    def milestones(self, set_milestones):
        attribute_path = DbTaskAttrPath().to_milestones()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_milestones)


    @property
    def start_date(self):
        attribute_path = DbTaskAttrPath().to_start_date()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @start_date.setter
    def start_date(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_start_date()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_start_date)

    @property
    def worked_days(self):
        attribute_path = DbTaskAttrPath().to_worked_days()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @worked_days.setter
    def worked_days(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_worked_days()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_start_date)

    @property
    def previous_artists(self):
        attribute_path = DbTaskAttrPath().to_previous_artists()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @previous_artists.setter
    def previous_artists(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_previous_artists()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_start_date)

    @property
    def status(self):
        attribute_path = DbTaskAttrPath().to_status()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @status.setter
    def status(self, set_status):
        attribute_path = DbTaskAttrPath().to_status()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_status)


    @property
    def data_schema(self) -> dict:
        attribute_path = DbEntityAttrPath().to_tasks()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @data_schema.setter
    def data_schema(self, tasks_schema: dict) -> None:
        if self.operation != DBAdd:
            attribute_path = DbEntityAttrPath().to_tasks()
            method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                            entry_id=self.current_entity_id,
                                            attribute=attribute_path), self.db_operation)
            method(tasks_schema)
        else:
            print(f"Not possible to use {self.operation.__name__}. Use only Set! Nothing DONE")

    @property
    def imports_from(self) -> list:
        attribute_path = DbTaskAttrPath().to_imports_from()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @imports_from.setter
    def imports_from(self, data_set) -> None:
        attribute_path = DbTaskAttrPath().to_imports_from()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        method(data_set)

    def output_slot(self, name):
        return TaskOutputSlot(operation=self.operation, db_operation=self.db_operation, name=name)

    def output_slots(self):
        return TaskOutputSlot(operation=self.operation, db_operation=self.db_operation)


class TaskOutputSlot:

    def __init__(self, operation=None, db_operation=None, name=None):
        self.operation = operation
        self.db_operation = db_operation
        self.output_name = name
        self.current_entity_id = DbIds.curr_entry_id()

    @property
    def out_slots_names(self) -> list:
        attribute_path = DbTaskAttrPath().to_pub_slots()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return list(results.keys())

    @property
    def data_schema(self):
        attribute_path = DbTaskAttrPath().to_pub_slots()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @data_schema.setter
    def data_schema(self, full_out_slots_data: dict):
        if self.operation != Add:
            attribute_path = DbTaskAttrPath().to_pub_slots()

            method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                            entry_id=self.current_entity_id,
                                            attribute=attribute_path), self.db_operation)

            method(full_out_slots_data)
        else:
            print(f"Not possible to use {self.operation.__name__}. Use only Set! Nothing DONE")

    @property
    def type(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_type()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @type.setter
    def type(self, type_name: str):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)

        method(type_name)

    @property
    def designation(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @designation.setter
    def designation(self, designation_name: str):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)

        method(designation_name)

    @property
    def is_active(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_active()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @is_active.setter
    def is_active(self, is_active: bool):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_active()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)

        method(is_active)

    @property
    def reviewable(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_reviewable()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @reviewable.setter
    def reviewable(self, is_reviewable: bool):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_reviewable()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)

        method(is_reviewable)

    @property
    def used_by(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_pub_slot_used_by()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @used_by.setter
    def used_by(self, input_data):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_pub_slot_used_by()

        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_entity_id,
                                        attribute=attribute_path), self.db_operation)

        method(input_data)


class AssetDefinition:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()

    def all(self):
        print("These are all definition elements of current asset")

    def element(self, name):
        print(f"{name} is a definition attribute")


class EntityParent:

    def db(self):
        print("I am the PARENT")

    def visual(self):
        print("I am the VISUAL_PARENT")

    def type(self):
        print("I am the TYPE")

    def add_to_visual_parent(self):
        pass


class Project:

    def __init__(self, operation=None, db_operation=None):
        self.db = MongoConnection().origin_production_database()
        self.operation = operation
        self.db_operation = db_operation
        self.current_proj_id = DbIds().curr_project_id()

    @property
    def project_type(self):
        attribute_path = DbProjectAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @project_type.setter
    def project_type(self, set_type):
        attribute_path = DbProjectAttrPath().to_type()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_type)

    @property
    def code(self):
        attribute_path = DbProjectAttrPath().to_code()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @code.setter
    def code(self, set_code):
        attribute_path = DbProjectAttrPath().to_code()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path),self.db_operation)
        method(set_code)

    @property
    def is_active(self):
        attribute_path = DbProjectAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbProjectAttrPath().to_is_active()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_is_active)

    @property
    def project_configuration(self) -> dict:
        attribute_path = DbProjectAttrPath().to_project_configuration()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @project_configuration.setter
    def project_configuration(self, config_data: dict):
        attribute_path = DbProjectAttrPath().to_project_configuration()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        method(config_data)

    @property
    def project_data(self):
        attribute_path = DbProjectAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        results = method()

        return results

    @project_data.setter
    def project_data(self, set_data):
        attribute_path = DbProjectAttrPath().to_data()
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.current_proj_id,
                                        attribute=attribute_path), self.db_operation)
        method(set_data)


class Projects:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation

    def names(self):
        delimiter = "__"

        projects_list = []
        get_all_in_database = FindInCollection().all_collections()
        for db_collection in get_all_in_database:
            if delimiter not in db_collection:
                projects_list.append(db_collection)

        return projects_list


class WorkFiles:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.db_collection = ProjectCollections().project_work_files_collection()
        # self.current_entity_id = DbIds.curr_entry_id()

    def all(self):
        print("These are all Work Files")

    def by_user(self):
        pass

    def by_date(self):
        pass

    def curr_task(self):
        pass

    def outdated_inputs(self):
        pass

    def my_work_files(self):
        pass


class TaskPublish:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation

    def all(self, limit=None):
        print("These are all publishes")

    def task(self):
        pass

    def owner(self):
        pass

    def date(self):
        pass

    def time(self):
        pass

    def status(self):
        pass

    def components(self):
        pass

    def thumbnail(self):
        pass

    def version(self):
        pass

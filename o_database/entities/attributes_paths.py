from envars.origin_envars import OriginEnvar
from database.utils import db_path_assembler


class DbProjectAttrPath:

    @classmethod
    def custom(cls, attr):
        """returns the @attr parameter as inputted"""
        return attr

    @classmethod
    def to_name(cls):
        """Access path project name property"""
        return "entry_name"

    @classmethod
    def to_curr_show(cls):
        return OriginEnvar().show_name

    @classmethod
    def to_is_active(cls):
        """Access path to is_active property of current project"""
        return "active"

    @classmethod
    def to_type(cls):
        """Access path to get project Type"""
        return "show_type"

    @classmethod
    def to_code(cls):
        """Access path to get project Type"""
        return "show_code"

    @classmethod
    def to_project_configuration(cls):
        return "config"

    @classmethod
    def to_data(cls):
        return "data"


class DbEntityAttrPath:

    @classmethod
    def to_assignment(cls):
        return "assignment"

    @classmethod
    def to_entry_definition(cls):
        return "definition"

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def to_is_active(cls):
        """Access path to get if an Entity is active"""
        return "active"

    @classmethod
    def to_type(cls):
        """Access path to get the Type of an Entity"""
        return "type"

    @classmethod
    def to_tasks(cls):
        """Access path for tasks of the entry"""
        return "tasks"

    @classmethod
    def sync_tasks(cls):
        """Access path for tasks of the entry"""
        return "sync_tasks"

    @classmethod
    def to_assignments(cls):
        """Access path for tasks of the entry"""
        return "assignment"

    @classmethod
    def to_assigned_to(cls):
        return "assigned_to"

    @classmethod
    def to_definition(cls, element=None):
        if element:
            return db_path_assembler.make_path("definition", element)
        """Access path for tasks of the entry"""
        return "definition"

    @classmethod
    def to_components(cls):
        return "components"

    @classmethod
    def to_config(cls):
        return "config"

    @classmethod
    def to_children(cls):
        return "children"

    @classmethod
    def to_visual_children(cls):
        return "visual_children"

    @classmethod
    def to_origin_db_path(cls):
        return "origin_db_path"

    @classmethod
    def to_visual_parent(cls):
        return "visual_parent"

    @classmethod
    def to_parent(cls):
        return "parent"

    @classmethod
    def to_data(cls):
        return "data"


class DbAssetAttrPath(DbEntityAttrPath):
    def __init__(self):
        super(DbAssetAttrPath, self).__init__()


class DbTaskAttrPath:
    def __init__(self):
        self.task_name = OriginEnvar.task_name

    @classmethod
    def custom(cls, attr):
        """returns the @attr parameter as inputted"""
        return attr

    @classmethod
    def to_is_active(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "active")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "active")

    @classmethod
    def to_status(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "status")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "status")

    @classmethod
    def to_artist(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "artist")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "artist")

    @classmethod
    def to_imports_from(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "imports_from")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "imports_from")

    @classmethod
    def to_pub_slots(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "pub_slots")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots")

    @classmethod
    def to_bid_days(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "bid_days")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "bid_days")

    @classmethod
    def to_end_date(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "end_date")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "end_date")

    @classmethod
    def to_milestones(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "milestones")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "milestones")

    @classmethod
    def to_start_date(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "start_date")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "start_date")

    @classmethod
    def to_worked_days(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "worked_days")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "worked_days")

    @classmethod
    def to_previous_artists(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "previous_artists")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "previous_artists")


class DbPubSlotsAttrPath:
    def __init__(self, publish_slot_name):
        self.pub_slot_name = publish_slot_name

    def custom(self, attr):
        """Access path to get the Type of an Entity"""
        return attr

    def to_is_active(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "active")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "active")

    def to_is_reviewable(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "reviewable")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "reviewable")

    def to_scope(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "scope")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "scope")

    def to_path_to_used_by(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "used_by")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "used_by")

    def to_method(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "method")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "method")

    def to_type(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "type")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, "pub_slots", self.pub_slot_name, "type")


    def to_pub_slot_used_by(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "used_by")
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, 'pub_slots', self.pub_slot_name, "used_by")

    @classmethod
    def to_pub_slot_needs(cls, pub_slot):
        return db_path_assembler.make_path("tasks", OriginEnvar.task_name, 'pub_slots', pub_slot, "needs")


class DbTaskPublishAttrPath:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def to_version(cls):
        return "version"

    @classmethod
    def to_entry_name(cls):
        return "entry_name"

    @classmethod
    def to_type(cls):
        return "type"

    @classmethod
    def to_description(cls):
        return "description"

    @classmethod
    def to_status(cls):
        return "status"

    @classmethod
    def to_components(cls):
        return "components"

    @classmethod
    def to_origin_db_path(cls):
        return "origin_db_path"

    @classmethod
    def to_children(cls):
        return "children"

    @classmethod
    def to_parent(cls):
        return "parent"

    @classmethod
    def to_visual_parent(cls):
        return "visual_parent"

    @classmethod
    def to_date(cls):
        return "date"

    @classmethod
    def to_time(cls):
        return "time"

    @classmethod
    def to_owner(cls):
        return "owner"


class DbWorkSessionAttrPath:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def to_version(cls):
        return "version"

    @classmethod
    def to_entry_name(cls):
        return "entry_name"

    @classmethod
    def to_type(cls):
        return "type"

    @classmethod
    def to_description(cls):
        return "description"

    @classmethod
    def to_status(cls):
        return "status"

    @classmethod
    def to_components(cls):
        return "components"

    @classmethod
    def to_origin_db_path(cls):
        return "origin_db_path"

    @classmethod
    def to_children(cls):
        return "children"

    @classmethod
    def to_parent(cls):
        return "parent"

    @classmethod
    def to_visual_parent(cls):
        return "visual_parent"

    @classmethod
    def to_date(cls):
        return "date"

    @classmethod
    def to_time(cls):
        return "time"

    @classmethod
    def to_owner(cls):
        return "owner"

    @classmethod
    def to_session_content(cls):
        return "session_content"


if __name__ == '__main__':
    OriginEnvar.show_name="Test"
    OriginEnvar.branch_name="assets"
    OriginEnvar.category="characters"
    OriginEnvar.entry_name="red_hulk"
    OriginEnvar.task_name="surfacing"

    # pp_path = pp.db_task_pub(relative=False, dict_packed=True)
    # print (pp_path)
    asset_id = DbTaskAttrPath.to_imports_from()


    print (asset_id)

    add = DbAssetAttrPath()
    cc = add.to_data()
    print(cc)

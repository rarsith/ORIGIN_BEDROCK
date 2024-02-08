from envars.envars import Envars
from database.utils import db_path_assembler


class DbAttrPaths:

    @classmethod
    def to_base(cls, dict_packed=False):
        if dict_packed:
            return db_path_assembler.make_path(show_name=Envars.show_name,
                                               branch_name=Envars.branch_name,
                                               category=Envars.category,
                                               entry_name=Envars.entry_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name)

    @classmethod
    def to_root_full(cls, dict_packed=False):
        if dict_packed:
            return db_path_assembler.make_path(show_name=Envars.show_name,
                                               branch_name=Envars.branch_name,
                                               category=Envars.category,
                                               entry_name=Envars.entry_name,
                                               task_name=Envars.task_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name)

    @classmethod
    def to_branch(cls, dict_packed=False):
        if dict_packed:
            return db_path_assembler.make_path(show_name=Envars.show_name,
                                               branch_name=Envars.branch_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name)

    @classmethod
    def to_category(cls, dict_packed=False):
        if dict_packed:
            return db_path_assembler.make_path(show_name=Envars.show_name,
                                               branch_name=Envars.branch_name,
                                               category=Envars.category)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category)

    @classmethod
    def to_entry(cls, dict_packed=False):
        if dict_packed:
            return db_path_assembler.make_path(show_name = Envars.show_name,
                                               branch_name = Envars.branch_name,
                                               category = Envars.category,
                                               entry_name = Envars.entry_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name)

    @classmethod
    def to_task(cls, relative=True):
        if relative:
            return db_path_assembler.make_path("tasks", Envars.task_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "tasks",
                                           Envars.task_name)

    @classmethod
    def to_sync_tasks(cls, relative=True):
        if relative:
            return "sync_tasks"

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "sync_tasks")

    @classmethod
    def to_task_imports_from(cls, relative=True):
        if relative:
            return db_path_assembler.make_path("tasks", Envars.task_name, "imports_from")

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "tasks",
                                           Envars.task_name,
                                           "imports_from")

    @classmethod
    def to_sync_task_slot(cls, relative=True):
        if relative:
            return db_path_assembler.make_path("sync_tasks", Envars.task_name)

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "sync_tasks",
                                           Envars.task_name)

    @classmethod
    def to_pub_slots(cls, relative=True):
        if relative:
            return db_path_assembler.make_path("tasks", Envars.task_name, 'pub_slots')

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "tasks",
                                           Envars.task_name,
                                           "pub_slots")

    @classmethod
    def to_pub_slot_used_by(cls, pub_slot, relative=True):
        if relative:
            return db_path_assembler.make_path("tasks", Envars.task_name, 'pub_slots', pub_slot, "used_by")

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "tasks",
                                           Envars.task_name,
                                           "pub_slots",
                                           pub_slot,
                                           "used_by")

    @classmethod
    def to_entry_definition(cls, relative=True):
        if relative:
            return "definition"
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "definition")

    @classmethod
    def to_master_bundle(cls, relative=True):
        if relative:
            return "master_bundle"

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "master_bundle")

    @classmethod
    def to_assignment(cls, relative=True):
        if relative:
            return "assignment"

        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "assignment")


class DbEntityAttrPaths:

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
    def master_bundle(cls):
        """Access path for tasks of the entry"""
        return "master_bundle"


class DbProjectAttrPaths:

    @classmethod
    def custom(cls, attr):
        """returns the @attr parameter as inputted"""
        return attr

    @classmethod
    def structure(cls):
        """Access path the full structure of the current project """
        return "structure"

    @classmethod
    def name(cls):
        """Access path project name property"""
        return "entry_name"

    @classmethod
    def curr_show(cls):
        return Envars().show_name

    @classmethod
    def branches(cls):
        """Access path to all branches of the current project"""
        return "structure"

    @classmethod
    def categories(cls):
        """Access path to all categories of the current branch"""
        access_path = db_path_assembler.make_path("structure", Envars.branch_name)
        return access_path

    @classmethod
    def curr_branch(cls, branch_name=Envars.branch_name):
        """Access path to current branch of the current project"""
        curr_branch_path = db_path_assembler.make_path("structure", branch_name)
        return curr_branch_path

    @classmethod
    def curr_category(cls):
        """Access path to current category of the current project"""
        curr_category_path = db_path_assembler.make_path("structure", Envars.branch_name, Envars.category)
        return curr_category_path

    @classmethod
    def category_entries(cls):
        """Access path for categories of the branch"""
        access_path = db_path_assembler.make_path("structure", Envars.branch_name, Envars.category)
        return access_path

    @classmethod
    def show_defaults(cls):
        """Access path for show_defaults attribute of the current project"""
        return "show_defaults"

    @classmethod
    def entry(cls):
        """Access path for entries referenced inside the category"""
        access_path = db_path_assembler.make_path("structure", Envars.branch_name, Envars.category)
        return access_path

    @classmethod
    def is_active(cls):
        """Access path to is_active property of current project"""
        return "active"

    @classmethod
    def type(cls):
        """Access path to get project Type"""
        return "show_type"


class DbTaskAttrPaths:
    def __init__(self):
        self.task_name = Envars.task_name


    @classmethod
    def custom(cls, attr):
        """returns the @attr parameter as inputted"""
        return attr

    @classmethod
    def is_active(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "active")
        return db_path_assembler.make_path("tasks", Envars.task_name, "active")

    @classmethod
    def status(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "status")
        return db_path_assembler.make_path("tasks", Envars.task_name, "status")

    @classmethod
    def artist(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "artist")
        return db_path_assembler.make_path("tasks", Envars.task_name, "artist")

    @classmethod
    def imports_from(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "imports_from")
        return db_path_assembler.make_path("tasks", Envars.task_name, "imports_from")

    @classmethod
    def pub_slots(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("tasks", task_name, "pub_slots")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots")


class DbSyncTaskAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def sync_pub_slots(cls, task_name=None):
        if task_name:
            return db_path_assembler.make_path("sync_tasks", task_name)
        return db_path_assembler.make_path("sync_tasks", Envars.task_name)


class DbMainPubAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def version(cls):
        return "version"


class DbPubSlotsAttrPaths:
    def __init__(self, publish_slot_name):
        self.pub_slot_name = publish_slot_name

    def custom(self, attr):
        """Access path to get the Type of an Entity"""
        return attr

    def is_active(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "active")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "active")

    def is_reviewable(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "reviewable")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "reviewable")

    def scope(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "scope")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "scope")

    def path_to_used_by(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "used_by")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "used_by")

    def method(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "method")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "method")

    def type(self, parent_task_name=None):
        if parent_task_name:
            return db_path_assembler.make_path("tasks", parent_task_name, "pub_slots", self.pub_slot_name, "type")
        return db_path_assembler.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "type")


class DbBundleAttrPaths:
    def __init__(self, pub_slot):
        self.pub_slot_name = pub_slot

    def _pub_slot(self):
        return self.pub_slot_name

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def is_active(cls):
        return db_path_assembler.make_path(cls._pub_slot, Envars.task_name,"active")

    @classmethod
    def is_reviewable(cls):
        return db_path_assembler.make_path(cls._pub_slot, Envars.task_name, "reviewable")

    @classmethod
    def used_by(cls):
        return db_path_assembler.make_path(cls._pub_slot, Envars.task_name, "used_by")

    @classmethod
    def method(cls):
        return db_path_assembler.make_path(cls._pub_slot, Envars.task_name, "method")

    @classmethod
    def type(cls):
        return db_path_assembler.make_path(cls._pub_slot, Envars.task_name, "type")



if __name__ == '__main__':
    Envars.show_name="Test"
    Envars.branch_name="assets"
    Envars.category="characters"
    Envars.entry_name="red_hulk"
    Envars.task_name="surfacing"

    # pp_path = pp.db_task_pub(relative=False, dict_packed=True)
    # print (pp_path)
    asset_id = DbTaskAttrPaths.imports_from()


    print (asset_id)

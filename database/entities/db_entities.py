from common_utils.date_time import DateTime
from common_utils.output_paths import OutputPaths
from common_utils.users import Users
from database.db_defaults import DbDefaults
from database.db_statuses import DbStatuses
from database.utils.db_version_control import DBVersionControl
from envars.envars import Envars
from database import db_connection as mdbconn, db_templates
from database.utils.db_q_entity import From, QEntity, DbRef, DbReferences
from database.entities.db_structures import DbProjectBranch
from database.entities.db_attributes import (DbAttrPaths,
                                             DbProjectAttrPaths,
                                             DbEntityAttrPaths,
                                             DbTaskAttrPaths,
                                             DbSyncTaskAttrPaths,
                                             DbPubSlotsAttrPaths)
from database.db_ids import DbIds
from database.utils import db_path_assembler


class _DbProjectCode:
    """Generates a unique code for the project"""
    data: str

    def __init__(self, data):
        self.data = data

    def code(self) -> str:
        addition = "this is a code" # TODO: build a code generator
        return self.data+"-"+addition


class _DbConstructors:

    def basic_constructor(self):
        version = DBVersionControl().db_wip_files_version_increase("work_files")
        common_id = DbIds.get_wip_file_id(version)
        entity_attributes = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            # entry_name=name,
            type=DbProjectBranch().get_current_branch_type,
            status=" ",
            assignment={},
            tasks=DbDefaults().get_show_defaults(DbDefaults().root_tasks),
            sync_tasks=DbSyncTasks().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active=True,
            definition=DbDefaults().get_show_defaults(DbDefaults().root_definitions),
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_attributes

    def _project_defaults(self):
        proj_defaults = dict(asset_definition=db_templates.entry_definition("build"),
                             shots_definition=db_templates.entry_definition("shot"),
                             characters_tasks=db_templates.tasks_schema("character"),
                             props_tasks=db_templates.tasks_schema("prop"),
                             environments_tasks=db_templates.tasks_schema("environment"),
                             characters_definition=db_templates.entry_definition("build"),
                             props_definition=db_templates.entry_definition("build"),
                             environments_definition=db_templates.entry_definition("build"),
                             shots_tasks=db_templates.tasks_schema("shot"))

        return proj_defaults

    def project_construct(self, name, entity_id, project_type="vfx"):
        entity_attributes = dict(
            _id=entity_id,
            show_code=_DbProjectCode(data=name).code(),
            entry_name=name,
            structure=db_templates.show_structure(),
            show_defaults=self._project_defaults(),
            active=True,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user(),
            show_type=project_type)

        return entity_id, entity_attributes

    @staticmethod
    def asset_construct(name, entity_id):
        entity_attributes = dict(
            _id=entity_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=name,
            type=DbProjectBranch().get_current_branch_type,
            status=" ",
            assignment={},
            assigned_to=[],
            tasks=DbDefaults().get_show_defaults(DbDefaults().root_tasks),
            sync_tasks=DbSyncTasks().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active=True,
            definition=DbDefaults().get_show_defaults(DbDefaults().root_definitions),
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_id, entity_attributes

    @staticmethod
    def work_session_construct(file_name):
        version = DBVersionControl().db_wip_files_version_increase("work_files")
        set_display_name = "_".join([Envars.entry_name, Envars.task_name, "work_file", version])
        common_id = DbIds.get_wip_file_id(version)

        save_content = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            status="WIP",
            description=[],
            artist=Users.curr_user(),
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="wip_scene",
            display_name=set_display_name,
            origin=[],
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session=[]
        )

        return common_id, save_content
        pass

    @staticmethod
    def bundle_construct():
        status = DbStatuses.pending_rev
        entity_tasks = DbTasks().get_tasks()
        version = DBVersionControl().db_master_bundle_ver_increase()
        common_id = DbIds.get_master_bundle_id(version)
        set_display_name = "_".join([Envars.entry_name, "bundle", version])

        entity_attributes = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            display_name=set_display_name,
            artist=Users.curr_user(),
            status=status,
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            master_bundle=dict.fromkeys(entity_tasks, [])
        )
        return common_id, entity_attributes

    @staticmethod
    def main_publish_construct():
        version = DBVersionControl().db_main_pub_ver_increase()
        set_display_name = "_".join([Envars.entry_name, "main_publish"])
        common_id = DbIds.get_main_pub_id(version)

        save_content = dict(
            _id=common_id,
            reviewable_component="insert_movie",
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            status="PENDING_REVIEW",
            description=[],
            artist=Users.curr_user(),
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="main",
            publishing_slots=[],
            display_name=set_display_name
        )

        return common_id, save_content

    @staticmethod
    def slot_publish_construct(pub_slot):
        collection_name = "_".join(["publish", "slots", Envars.task_name])
        version = DBVersionControl().db_pubslot_ver_increase(collection_name, pub_slot)
        set_display_name = "_".join(["pubslot", pub_slot, Envars.task_name])
        build_server_path = [Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             version,
                             pub_slot]

        common_id = DbIds.get_pub_slot_id(pub_slot, version)
        bundle = 'current_bundle'

        save_content = dict(
            _id=common_id,
            reviewable_component="insert_movie_path",
            slot_thumbnail="insert_thumbnail_path",
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            update_type="non-critical",
            artist=Users.curr_user(),
            slot_name=pub_slot,
            status="PENDING-REVIEW",
            version_origin="created",
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="slots",
            parent_collection=collection_name,
            display_name=set_display_name,
            output_path=build_server_path,
            components=dict(path=OutputPaths(version, pub_slot, "cache.abc").main_publish_path(),
                            rc_source_images=OutputPaths(version, pub_slot, "image.%04d.exr").original_images_path(),
                            rc_source_video=OutputPaths(version, pub_slot, "video.mov").review_video_path(),
                            rc_preview=OutputPaths(version, pub_slot, "video.mov").preview_video_path(),
                            template=OutputPaths().used_template_path(),
                            work_file=OutputPaths(version, "work_scene.ext").work_file_path(),
                            chain=OutputPaths().origin(),
                            bundle=bundle,
                            rc_output_path="_path"))

        return common_id, save_content

    @staticmethod
    def sync_tasks_capture_construct(current_syncs: dict):
        # TODO: cohesion check!!
        version = DBVersionControl().db_sync_tasks_ver_increase()
        entity_id = DbIds.get_sync_tasks_id(version)

        entity_attributes = dict(
            _id=entity_id,
            show_name=Envars.show_name,
            entry_name=Envars.entry_name,
            category=Envars.category,
            version=version,
            sync_tasks=current_syncs,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_id, entity_attributes


class DbProject:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    @staticmethod
    def current():
        return Envars().show_name

    def create(self, name):
        entity_id = db_path_assembler.make_path("root", name)
        created_id, save_data = _DbConstructors().project_construct(name=name, entity_id=entity_id)

        try:
            self.db.show.insert_one(save_data)
            print("{} Project created!".format(name))

        except ValueError as e:
            print("{} Error! Nothing created!".format(e))

    def get_all(self):
        """Returns all assets names in the current category"""
        try:
            result = QEntity(From().projects,
                             DbIds.all_in_collection(),
                             DbProjectAttrPaths.name()
                             ).get(all=True)
            return result
        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_structure():
        try:
            structure = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.structure()
                                ).get_attr_values()
            return structure

        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_entities_names():
        entities_found = list()

        origin_q = QEntity(From().projects,
                           DbIds.curr_project_id(),
                           DbProjectAttrPaths.category_entries()
                           ).get(attrib_names=True)

        for entity in origin_q:
            name = DbRef().db_deref(ref_string=entity, get_field="entry_name")
            entities_found.append(name)

        return entities_found

    @staticmethod
    def get_type():
        try:
            show_type = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.type()
                                ).get(attrib_names=True)
            return show_type
        except ValueError as val:
            print ("{} Nothing Done!".format(val))

    @staticmethod
    def is_active():
        try:
            is_active = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.is_active()
                                ).get(attrib_names=True)
            return is_active
        except ValueError as val:
            print ("{} Nothing Done!".format(val))


class DbAsset:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        collection = self.db[From().entities]
        created_id, save_data = _DbConstructors().asset_construct(name=name,
                                                                  entity_id=DbIds.create_entity_id(name))

        try:
            collection.insert_one(save_data)

            insert_entry = db_path_assembler.make_path("structure",
                                                        Envars().branch_name,
                                                        Envars().category)

            DbReferences.add_db_id_reference(collection="show",
                                             parent_doc_id=DbIds.curr_project_id(),
                                             destination_slot=insert_entry,
                                             id_to_add=created_id,
                                             from_collection=DbProjectBranch().get_current_branch_type,
                                             replace=False)

            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_all(self, is_active=True):
        """Returns all assets names in the current category"""
        try:
            result = QEntity(db_collection=From().projects,
                             entry_id=DbIds.curr_project_id(),
                             attribute_path=DbProjectAttrPaths.category_entries()
                             ).get(attrib_names=True, all_active=is_active)
            return result
        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    def get_anything(self, attrib):
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute_path=attrib
                             ).get_attr_names()
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_definition():
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute_path=DbEntityAttrPaths.to_definition()
                             ).get_attr_values()
            if not result:
                return ""
            return result

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_definition_element(definition_element):
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute_path=DbEntityAttrPaths.to_definition(element=definition_element)
                             ).get_attr_names()
            return result
        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_entry_type():
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute_path=DbEntityAttrPaths.to_type()
                             ).get_attr_names()
            if not result:
                return ""
            return result

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @property
    def entities_assigned(self):
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute_path=DbEntityAttrPaths.to_assignments()
                             ).get_attr_names()
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @entities_assigned.setter
    def entities_assigned(self, assigned_list):
        try:
            for each in assigned_list:
                QEntity(db_collection=From().entities,
                        entry_id=DbIds.curr_entry_id(),
                        attribute_path=DbEntityAttrPaths.to_assignments()
                        ).add(data=each)
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    def rem_entities_assinged(self):
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbEntityAttrPaths.to_assignments()
                    ).clear(override=True)
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @staticmethod
    def set_active(is_active=True):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbEntityAttrPaths.to_is_active()
                ).update(is_active)

        print("{0} active Status set to {1}!".format(DbIds.curr_entry_id(), is_active))

    @staticmethod
    def set_definition(data):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbEntityAttrPaths.to_definition
                ).update(data)
        print("{} Definition Updated!".format(Envars.entry_name))

    def remove(self):
        #TODO: refactor code to use fully the Envars
        try:
            QEntity(db_collection=From().projects,
                    entry_id=DbIds.curr_project_id(),
                    attribute_path=DbProjectAttrPaths.entry()
                    ).remove()

            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbEntityAttrPaths.to_type()
                    ).remove()

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))


class DbTasks:

    def create(self, name):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbEntityAttrPaths.to_tasks()
                ).add_property(name=name, add_data=db_templates.task_defaults())

        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbEntityAttrPaths.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Origin Asset Task created!".format(name))
        return name

    def get_tasks(self) -> list:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute_path=DbEntityAttrPaths.to_tasks()
                                 ).get_attr_names()

            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def get_tasks_full(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute_path=DbEntityAttrPaths.to_tasks()
                                 ).get()

            return tasks_list
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def current_is_active(self) -> bool:
        try:
            is_active_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbTaskAttrPaths.is_active()
                                     ).get_attr_values()
            return is_active_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @current_is_active.setter
    def current_is_active(self, is_active: bool) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.is_active()
                    ).update(data=is_active)

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def is_active(self, task: str) -> bool:
        try:
            is_active_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbTaskAttrPaths.is_active(task_name=task)
                                     ).get_attr_values()
            return is_active_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def set_active(self, task: str, is_active: bool) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.is_active(task_name=task)
                    ).update(data=is_active)

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def status(self) -> str:
        try:
            status_data = QEntity(db_collection=From().entities,
                                  entry_id=DbIds.curr_entry_id(),
                                  attribute_path=DbTaskAttrPaths.status()
                                  ).get_attr_values()
            return status_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @status.setter
    def status(self, task_status: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbTaskAttrPaths.status()
                ).update(data=task_status)

    @property
    def task_user(self) -> str:
        user = QEntity(db_collection=From().entities,
                       entry_id=DbIds.curr_entry_id(),
                       attribute_path=DbTaskAttrPaths.artist()
                       ).get_attr_values()
        return user

    @task_user.setter
    def task_user(self, artist_name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbTaskAttrPaths.artist()
                ).update(data=artist_name)

    @property
    def imports_from(self) -> list:
        try:
            imports_from_data = QEntity(db_collection=From().entities,
                                        entry_id=DbIds.curr_entry_id(),
                                        attribute_path=DbTaskAttrPaths.imports_from()
                                        ).get_attr_values()
            return imports_from_data
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @imports_from.setter
    def imports_from(self, imports_from: list) -> None:
        for each in imports_from:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.imports_from()
                    ).add(data=each)
            # print("{} task added as import_source".format(each))

    def rem_import_slots(self) -> None:
        #TODO implement deleter property
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.imports_from()
                    ).clear(override=True)
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))


class DbPublish:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def get_db_publishes_ids(self, collection, view_limit=0):
        #TODO change this to database aggregations
        store_value = list()
        cursor = self.db[collection]
        curr_envars_set = Envars().get_envars_set()

        test = cursor.find(curr_envars_set).limit(view_limit)

        for publishes in test:
            store_value.append(str(publishes["_id"]))
        return store_value

    def get_db_values(self, collection, document_id, value_to_return):
        if not collection or not document_id or collection == None or document_id == None:
            return
        else:
            selected_document = self.db[collection].find_one({"_id": document_id})
            return selected_document[value_to_return]

    def db_main_publish(self):
        version = DBVersionControl().db_main_pub_ver_increase()
        set_display_name = "_".join([Envars.entry_name, "main_publish"])

        common_id = DbIds.get_main_pub_id(version)
        collection_name = "publishes"

        save_content = dict(
            _id= common_id,
            reviewable_component= "insert_movie",
            show_name= Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name= Envars.entry_name,
            task_name= Envars.task_name,
            status= "PENDING_REVIEW",
            description= [],
            artist= Users.curr_user(),
            version= version,
            date= DateTime().curr_date,
            time= DateTime().curr_time,
            publish_packaging= "main",
            publishing_slots= [],
            display_name= set_display_name
        )

        published = self.db[collection_name].insert_one(save_content)

        print("{0} Main Publish Done!".format(set_display_name))
        return published.inserted_id, collection_name

    def db_slot_publish(self, pub_slot):
        #TODO check if slot is active

        collection_name = "_".join(["publish", "slots", Envars.task_name])
        version = DBVersionControl().db_pubslot_ver_increase(collection_name, pub_slot)
        set_display_name = "_".join(["pubslot", pub_slot, Envars.task_name])
        build_server_path = [Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             version,
                             pub_slot]

        common_id = DbIds.get_pub_slot_id(pub_slot, version)
        bundle = 'current_bundle'

        save_content = dict(
            _id=common_id,
            reviewable_component = "insert_movie_path",
            slot_thumbnail= "insert_thumbnail_path",
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            update_type="non-critical",
            artist= Users.curr_user(),
            slot_name= pub_slot,
            status= "PENDING-REVIEW",
            version_origin= "created",
            version= version,
            date= DateTime().curr_date,
            time= DateTime().curr_time,
            publish_packaging= "slots",
            parent_collection= collection_name,
            display_name= set_display_name ,
            output_path= build_server_path,
            components= dict(path=OutputPaths(version, pub_slot, "cache.abc").main_publish_path(),
                             rc_source_images=OutputPaths(version, pub_slot, "image.%04d.exr").original_images_path(),
                             rc_source_video= OutputPaths(version, pub_slot, "video.mov").review_video_path(),
                             rc_preview= OutputPaths(version, pub_slot, "video.mov").preview_video_path(),
                             template= OutputPaths().used_template_path(),
                             work_file= OutputPaths(version, "work_scene.ext").work_file_path(),
                             chain= OutputPaths().origin(),
                             bundle= bundle,
                             rc_output_path="_path"))

        published_slot = self.db[collection_name].insert_one(save_content)

        print("{0} slot {1} has been published".format(pub_slot, version))
        return published_slot.inserted_id, collection_name

    def db_publish(self):
        task_pub_slots = DbPubSlot().get_pub_slots()
        current_task = Envars().task_name

        main_publish = self.db_main_publish()
        for pub_slot in task_pub_slots:

            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])

            pub_slots_publish = self.db_slot_publish(pub_slot)

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                             parent_doc_id=main_publish[0],
                                             destination_slot="publishing_slots",
                                             id_to_add=pub_slots_publish[0],
                                             from_collection=pub_slots_publish[1])

            DbReferences.add_db_id_reference(collection=DbProjectBranch().get_current_branch_type,
                                             parent_doc_id=DbIds.curr_entry_id(),
                                             destination_slot=get_sync_path,
                                             id_to_add=pub_slots_publish[0],
                                             from_collection=pub_slots_publish[1],
                                             replace=True)

        return main_publish

    def db_publish_sel(self, sel_pub_slots=[]):
        current_task = Envars().task_name
        task_pub_slots = DbPubSlot().get_pub_slots()
        get_sync_tasks = DbSyncTasks().capture_all()
        sync_to_curr_task = get_sync_tasks[current_task]

        if len(sel_pub_slots)==0:
            sel_pub_slots = task_pub_slots

        for sync_slot in sel_pub_slots:
             del sync_to_curr_task[sync_slot]

        main_publish = self.db_main_publish()

        for pub_slot in sel_pub_slots:
            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])
            pub_slots_publish = self.db_slot_publish(pub_slot)

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                             parent_doc_id=main_publish[0],
                                             destination_slot="publishing_slots",
                                             id_to_add=pub_slots_publish[0],
                                             from_collection=pub_slots_publish[1])

            DbReferences.add_db_id_reference(collection=DbProjectBranch().get_current_branch_type,
                                             parent_doc_id=DbIds.curr_entry_id(),
                                             destination_slot=get_sync_path,
                                             id_to_add=pub_slots_publish[0],
                                             from_collection=pub_slots_publish[1],
                                             replace=True)

        for inherited_slot in sync_to_curr_task.items():
            get_collection = inherited_slot[1].split(",")

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                             parent_doc_id=main_publish[0],
                                             destination_slot="publishing_slots",
                                             id_to_add=get_collection[1],
                                             from_collection=get_collection[0])

        return main_publish

    def db_work_file_save(self, file_name):
        version = DBVersionControl().db_wip_files_version_increase("work_files")
        set_display_name = "_".join([Envars.entry_name,Envars.task_name, "work_file", version])

        common_id = DbIds.get_wip_file_id(version)
        collection_name = "work_files"

        save_content = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            status="WIP",
            description=[],
            artist=Users.curr_user(),
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="wip_scene",
            display_name=set_display_name,
            origin=[],
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session=[]
        )

        published = self.db[collection_name].insert_one(save_content)

        print("{0} Saved!".format(set_display_name))
        return published.inserted_id, collection_name

    def publish_sync_state(self):
        #TODO: cohesion check!!
        existing_sync_tasks = self.capture_all()
        version = DBVersionControl().db_sync_tasks_ver_increase()
        entity_id = DbIds.get_sync_tasks_id(version)
        entity_attributes = dict(
            _id= entity_id,
            show_name= Envars.show_name,
            entry_name= Envars.entry_name,
            category= Envars.category,
            version=version,
            sync_tasks= existing_sync_tasks,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner= Users.curr_user()
        )
        try:
            self.db.sync_tasks.insert_one(entity_attributes)

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))


class DbPubSlot:
    def create(self, name: str) -> str:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbTaskAttrPaths.pub_slots()
                ).add_property(name=name, add_data=db_templates.tasks_pub_slot_schema())

        DbSyncTasks().add_sync_task_slot(name)
        print("{} Task Pub Slot created!".format(name))
        return name

    def add_multiple(self, pub_slot: list) -> None:
        for each in pub_slot:
            self.create(each)
            print("{} added as pub_slot".format(each))

    def add_dict(self, pub_slot: list) -> None:
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))

            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.pub_slots()
                    ).add_property(name=get_slot_name[0], add_data=get_slot_param[0])

        print("Publish Slot added succesfully!")

    def get_pub_slots(self, task_name=None) -> dict:
        if task_name:
            try:
                pub_slots_data = QEntity(db_collection=From().entities,
                                         entry_id=DbIds.curr_entry_id(),
                                         attribute_path=DbTaskAttrPaths.pub_slots(task_name=task_name)
                                         ).get_attr_values()
                return pub_slots_data

            except Exception as e:
                print("{} Error! Nothing Created!".format(e))

        else:
            try:
                pub_slots_data = QEntity(db_collection=From().entities,
                                         entry_id=DbIds.curr_entry_id(),
                                         attribute_path=DbTaskAttrPaths.pub_slots()
                                         ).get_attr_values()
                return pub_slots_data

            except Exception as e:
                print("{} Error! Nothing Created!".format(e))

    def get_type(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).type()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_method(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).method()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_used_by(self, pub_slot: str) -> list:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).path_to_used_by()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_used_by_task(self, data, task_name=None):
        get_pub_slots = []
        get_slots = list(data.keys())

        if task_name:
            for x in get_slots:
                if task_name in data[x]['used_by']:
                    get_pub_slots.append(x)
            return get_pub_slots

        task_name = Envars().task_name
        for x in get_slots:
            if task_name in data[x]['used_by']:
                get_pub_slots.append(x)
        return get_pub_slots

    def get_is_reviewable(self, pub_slot: str) -> bool:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).is_reviewable()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_is_active(self, pub_slot: str) -> None:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).is_active()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def set_used_by(self, task_name: str, pub_slot: str, used_by_data: str = None, remove_action: bool = False) -> None:
        existing_used_by_data = QEntity(db_collection=From().entities,
                                        entry_id=DbIds.curr_entry_id(),
                                        attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).path_to_used_by(
                                            parent_task_name=task_name)
                                        ).get_attr_values()
        if not remove_action:
            if used_by_data not in existing_used_by_data:
                QEntity(db_collection=From().entities,
                        entry_id=DbIds.curr_entry_id(),
                        attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).path_to_used_by(parent_task_name=task_name)
                        ).add(data=used_by_data)

        else:
            if used_by_data in existing_used_by_data:
                QEntity(db_collection=From().entities,
                        entry_id=DbIds.curr_entry_id(),
                        attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).path_to_used_by(parent_task_name=task_name)
                        ).remove_value(data=used_by_data)

    def remove_all(self) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute_path=DbTaskAttrPaths.pub_slots(),
                    ).clear()

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_pub_slots_scope(self, pub_slot: str):
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute_path=DbPubSlotsAttrPaths(publish_slot_name=pub_slot).scope()
                                     ).get_attr_values()
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))


class DbSyncTasks:
    @staticmethod
    def create_from_template():
        get_tasks_config = DbDefaults().get_show_defaults(DbDefaults().root_tasks)
        entity_tasks = list(get_tasks_config)
        save_elements_list = dict()
        for task in entity_tasks:
            task_definition = (get_tasks_config[task])
            task_pub_slots = (list(task_definition["pub_slots"].keys()))
            make_dictionary = dict.fromkeys(task_pub_slots, {})
            nest_slot = {task: make_dictionary}
            save_elements_list.update(nest_slot)

        return save_elements_list

    def capture_all(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute_path=DbEntityAttrPaths.sync_tasks()
                                 ).get_attr_values()
            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def add(self, data: dict):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbEntityAttrPaths.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute_path=DbSyncTaskAttrPaths.sync_pub_slots()
                ).add_property(name=name, add_data={})

        print("{} Sync Slot saved!".format(name))

    def get_sync_task_slots(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute_path=DbSyncTaskAttrPaths.sync_pub_slots()
                                 ).get_attr_values()

            return tasks_list

        except ValueError as vale:
            print(vale)


class DbBundle:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self):
        inserted_id, save_content = _DbConstructors().bundle_construct()
        master_bundle = self.db.bundles.insert_one(save_content)
        print("{0}, has been published".format(inserted_id))
        return master_bundle.inserted_id

    def create_stream(self, name):
        try:
            asset_id = DbIds.curr_entry_id()
            cursor = self.db[DbProjectBranch().get_current_branch_type]
            db_path = db_path_assembler.make_path(DbAttrPaths.to_master_bundle(),
                                                  (name + "_" + "stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except ValueError as e:
            print("{} Error! Nothing Created!".format(e))

    @staticmethod
    def add_to_bundle(entity_id, bundle_id, slot):
        DbReferences.add_db_id_reference("bundles",
                                         bundle_id,
                                         "master_bundle.{}".format(slot),
                                         entity_id,
                                         DbProjectBranch().get_current_branch_type,
                                         replace=True)
        return bundle_id

    def add_slot(self, name):
        pass

    def rem_slot(self, name):
        pass

    def update_slot(self, name):
        pass

    def update_master(self):
        pass

    @staticmethod
    def set_as_current(bundle_id, add_to_stream="main_stream"):

        DbReferences.add_db_id_reference(DbProjectBranch().get_current_branch_type,
                                         DbIds.curr_entry_id(),
                                         "master_bundle.{}".format(add_to_stream),
                                         bundle_id,
                                         "bundles",
                                         replace=True)
        return bundle_id

    def set_slot_state(self, state):
        statuses = ["renderable", "matte_object"]
        pass

    def validate_bundle(self):
        pass

    def health_check(self):
        pass

    def mv_to_stream(self, from_stream, to_stream):
        #TODO: finish the method
        try:
            task_path = DbAttrPaths.to_pub_slots()
            print(task_path)
            cursor = self.db[DbProjectBranch().get_current_branch_type]
            cursor.update_one({"_id": DbIds.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


if __name__ == '__main__':
    import pprint

    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "frog"
    Envars.task_name = "rigging"

    # print (Envars().branch_name)
    # print (Envars().show_name)

    definition ={"crap":"mofo"}


    # xx = DbProject().create(name="GooGoo")
    # print (xx)

    # used_by_data = QEntity(db_collection=From().entities,
    #                        entry_id=DbIds.curr_entry_id(),
    #                        attribute=DbPubSlotsAttrPaths(publish_slot="rend_geo").used_by()
    #                        ).get_attr_values()

    # pubs = DbPubSlot().get_used_by("img")
    # print (pubs)

    xxx = DbProject().get_structure()
    for k, v in xxx.items():
        # print(xxx[k]["type"])
        # x = k["type"]
        # print(x)
        if xxx[k]["type"]=="shots":
            pprint.pprint(v)




from origin.database.entities.actions import Create
from origin.database.entities.types import TaskTypes
from origin.envars.origin_envars import ContextHandler


class TasksTemplates:
    asset_basic_tasks_config = {}

    shot_basic_tasks_config = {}

    def __init__(self, context: dict | ContextHandler):

        if isinstance(context, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(context)
        else:
            self.context_handler = context

    def create_build_tasks(self):
        created_tasks = []
        for task_name, task_type in self.asset_basic_tasks_config.items():
            task_id = Create(context=self.context_handler).task(name=task_name,
                                                                parent=self.context_handler.entity_id,
                                                                task_type=task_type)
            created_tasks.append(task_id)

        return created_tasks

    def create_shot_tasks(self):
        created_tasks = []
        for task_name, task_type in self.shot_basic_tasks_config.items():
            task_id = Create(context=self.context_handler).task(name=task_name,
                                                                parent=self.context_handler.entity_id,
                                                                task_type=task_type)
            created_tasks.append(task_id)

        return created_tasks

    def build_base_task_schema(self):
        self.asset_basic_tasks_config = {"modeling": TaskTypes().modeling(),
                                         "texturing": TaskTypes().texturing(),
                                         "rigging": TaskTypes().rigging(),
                                         "lookdev": TaskTypes().shading()}

    def build_has_groom(self):
        self.asset_basic_tasks_config.update({"groom": TaskTypes().groom()})

    def build_has_groom_cfx(self):
        self.asset_basic_tasks_config.update({"hair_sim": TaskTypes().character_fx()})

    def build_has_cloth_cfx(self):
        self.asset_basic_tasks_config.update({"cfx_set": TaskTypes().character_fx()})

    def build_is_assembly(self):
        self.asset_basic_tasks_config = {"assembly": TaskTypes().assembly(),
                                         "lookdev": TaskTypes().shading()}

    def shot_base_tasks(self):
        self.shot_basic_tasks_config = {"plate": TaskTypes().plate(),
                                        "tracking": TaskTypes().tracking(),
                                        "rotomation": TaskTypes().rotomation(),
                                        "layout": TaskTypes().layout(),
                                        "animation": TaskTypes().animation(),
                                        "lighting": TaskTypes().lighting(),
                                        "rendering": TaskTypes().rendering(),
                                        "comp": TaskTypes().compositing(),
                                        "roto": TaskTypes().compositing(),
                                        "paint": TaskTypes().compositing(),
                                        "editorial": TaskTypes().editorial(),
                                        }
        self.create_shot_tasks()

    def shot_has_cfx(self):
        self.shot_basic_tasks_config.update({"cfx": TaskTypes().character_fx()})
        self.create_shot_tasks()

    def shot_has_fx(self):
        self.shot_basic_tasks_config.update({"fx": TaskTypes().fx()})
        self.create_shot_tasks()

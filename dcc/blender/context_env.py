import os
from origin.envars import ContextHandler


def get_context_env():
    context_env = dict(
        session_filename=os.getenv('SESSION_FILENAME'),
        session_id=os.getenv('SESSION_ID'),
        show_name=os.getenv('SHOW_NAME'),
        project_publishes=os.getenv('PROJECT_PUBLISHES'),
        project_work=os.getenv('PROJECT_WORK'),
        project_control=os.getenv('PROJECT_CONTROL'),
        origin_path_hierarchy=os.getenv('ORIGIN_PATH_HIERARCHY'),
        entity_name=os.getenv('ENTITY_NAME'),
        entity_type=os.getenv('ENTITY_TYPE'),
        entity_id=os.getenv('ENTITY_ID'),
        task_name=os.getenv('TASK_NAME'),
        task_type=os.getenv('TASK_TYPE')
    )
    return context_env


SESSION = get_context_env()
CURRENT_SESSION = ContextHandler()
CURRENT_SESSION.load_session(SESSION)

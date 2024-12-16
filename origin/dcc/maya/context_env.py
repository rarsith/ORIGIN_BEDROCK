import os
import pprint

from origin.envars.origin_envars import ContextHandler


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
        task_type=os.getenv('TASK_TYPE'),
        task_id=os.getenv('TASK_ID'),
        db_asset_stream_id=os.getenv('DB_ASSET_STREAM_ID'),
        db_asset_type=os.getenv('DB_ASSET_TYPE'),
        db_asset_id=os.getenv('DB_ASSET_ID'),
        db_asset_version_id=os.getenv('DB_ASSET_VERSION_ID'),
        asset_breakdown_id=os.getenv('ASSET_BREAKDOWN_ID')
        
    )
    return context_env


__SESSION = get_context_env()
CURRENT_SESSION = ContextHandler()
CURRENT_SESSION.load_session(__SESSION)

# pprint.pprint(CURRENT_SESSION.snapshot_session())

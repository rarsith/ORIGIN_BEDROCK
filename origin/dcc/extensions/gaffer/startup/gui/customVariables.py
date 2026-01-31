import os
import IECore
import Gaffer


def get_context_env():
    context_env = dict(
        origin_projects_root = os.getenv('ORIGIN_PROJECTS_ROOT'),
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


def __scriptAdded( container, script ) :
    origin_envars = get_context_env()

    variables = script["variables"]

    for envar, envar_val in origin_envars.items() :
        if envar not in variables :
            resource = variables.addMember(envar, IECore.StringData( str(envar_val) if envar_val is not None else "" ), envar)

        Gaffer.MetadataAlgo.setReadOnly( variables[envar]["name"], True )


application.root()["scripts"].childAddedSignal().connect( __scriptAdded )
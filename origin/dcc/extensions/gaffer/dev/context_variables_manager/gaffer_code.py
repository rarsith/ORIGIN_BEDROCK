import os


def get_context_env():
    return dict(
        origin_projects_root=os.getenv("ORIGIN_PROJECTS_ROOT"),
        session_filename=os.getenv("SESSION_FILENAME"),
        session_id=os.getenv("SESSION_ID"),
        show_name=os.getenv("SHOW_NAME"),
        project_publishes=os.getenv("PROJECT_PUBLISHES"),
        project_work=os.getenv("PROJECT_WORK"),
        project_control=os.getenv("PROJECT_CONTROL"),
        origin_path_hierarchy=os.getenv("ORIGIN_PATH_HIERARCHY"),
        entity_name=os.getenv("ENTITY_NAME"),
        entity_type=os.getenv("ENTITY_TYPE"),
        entity_id=os.getenv("ENTITY_ID"),
        task_name=os.getenv("TASK_NAME"),
        task_type=os.getenv("TASK_TYPE"),
        task_id=os.getenv("TASK_ID"),
        db_asset_stream_id=os.getenv("DB_ASSET_STREAM_ID"),
        db_asset_type=os.getenv("DB_ASSET_TYPE"),
        db_asset_id=os.getenv("DB_ASSET_ID"),
        db_asset_version_id=os.getenv("DB_ASSET_VERSION_ID"),
        asset_breakdown_id=os.getenv("ASSET_BREAKDOWN_ID"),
    )


origin_variablesX = ['imageCataloguePort', 'projectName', 'projectRootDirectory', 'renderPass']

root_vars = root["variables"]


def remove_origin_context_vars()


    for var in root_vars.children():
        # origin_variables.append(var.getName())
        print(var.getName())
        var_name = var.getName()
        if var_name not in origin_variablesX:
            root_vars.removeChild(var)


def create_origin_context_vars():
    get_orig_ctx = get_context_env()

    for ctx_name, cx_val in get_orig_ctx.items():
        root_vars.addChild(Gaffer.NameValuePlug(ctx_name, Gaffer.StringPlug("value", defaultValue=str(cx_val))))


remove_origin_context_vars()
create_origin_context_vars()
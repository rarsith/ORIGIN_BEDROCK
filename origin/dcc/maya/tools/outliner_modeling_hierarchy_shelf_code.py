import os
import maya.cmds as cmds
import alembic.Abc


def create_modeling_template():
    main_container = cmds.group(em=True, name="main")
    slot_name = cmds.group(em=True, parent=main_container, name="geo")
    render_group = cmds.group(em=True, parent=slot_name, name="C_render_0001_GRP")
    proxy_group = cmds.group(em=True, parent=slot_name, name="C_proxy_0001_GRP")
    cmds.select(clear=True)


if __name__ == "__main__":
    create_modeling_template()
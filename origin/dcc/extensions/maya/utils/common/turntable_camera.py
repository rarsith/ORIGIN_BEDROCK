import importlib
import maya.cmds as cmds
from origin.envars.origin_envars import ContextHandler

def clone_environment():
    from origin.dcc.common.utils import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def get_entity_definition():
    context_handler = clone_environment()
    entity_doc = context_handler.database_handler().get_asset_document()
    entity_definition = entity_doc.definition

    return entity_definition


def create_camera():
    entity_definition = get_entity_definition()
    film_aspect_ratio = int(entity_definition["res_x"]) / int(entity_definition["res_y"])

    v_aperture = 0.945
    h_aperture = film_aspect_ratio * v_aperture

    turntable_cam = cmds.camera(n="camera",
                                centerOfInterest=5,
                                focalLength=50,
                                lensSqueezeRatio=1,
                                cameraScale=1,
                                horizontalFilmAperture=h_aperture,
                                verticalFilmAperture=v_aperture,
                                horizontalFilmOffset=0,
                                verticalFilmOffset=0,
                                filmFit="Fill",
                                overscan=1,
                                motionBlur=0,
                                shutterAngle=144,
                                nearClipPlane=0.1,
                                farClipPlane=10000,
                                orthographic=False,
                                orthographicWidth=30,
                                panZoomEnabled=0,
                                horizontalPan=0,
                                verticalPan=0,
                                zoom=1
                                )
    return turntable_cam[0]


def add_object_to_namespace(object_name, namespace_id):
    # Esure object name exists
    if not cmds.objExists(object_name):
        print("Object Not Found")
        return
    # Esure namespace exists
    if not cmds.namespace(exists=namespace_id):
        print("Namespace Not Found")
        return

    # cmds.namespace(set=":")
    cmds.namespace(set=namespace_id)
    cmds.rename(object_name, f':{namespace_id}:{object_name}')


def create_and_set_namespace(namespace):
    if not cmds.namespace(exists=namespace):
        cmds.namespace(add=namespace)
    cmds.namespace(set=":")
    # Set the namespace to the desired one

    return namespace


def main():
    camera_name = create_camera()
    namespace_camera_ns = create_and_set_namespace("turntable_camera")
    add_object_to_namespace(object_name=camera_name, namespace_id=namespace_camera_ns)

    cmds.namespace(set=":")
    cmds.select(cl=True)

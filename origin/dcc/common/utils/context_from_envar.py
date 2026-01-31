import importlib
from origin.envars.origin_envars import ContextHandler
from origin.dcc.common.utils import context_env


def clone_environment():
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)

    return CLONED_CONTEXT

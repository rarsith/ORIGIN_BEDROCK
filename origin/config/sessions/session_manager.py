import os
from pathlib import Path

from origin.common_utils.json_utils import open_json, write_json, save_json
from origin.envars.origin_envars import ContextHandler


class SessionManager:
    def __init__(self):
        origin_root = Path(os.getenv("ORIGIN_ROOT"))
        self.session_file_path = origin_root / Path("origin/config/sessions/last_session.json")
        self.last_session = open_json(str(self.session_file_path))

        self.snapshot_session = None

    def get_last_session(self):
        return self.last_session

    def received_context(self, context: ContextHandler):
        self.snapshot_session = context.resolve_to_full_context()

    def save_last_session(self, session=None):

        get_root_path = os.path.split(self.session_file_path)[0]

        if session is not None:
            session_file = {"show_name": session}

            save_json(get_root_path, data=session_file, target_file="last_session.json")

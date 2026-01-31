import os
from pathlib import Path
from origin.common_utils.users import Users
from origin.database.entities.operators import get_file_component_class
from origin.paths.naming import AssetNaming


class OriginPathBuilder:
    PUBLISH_ROOT = "publishes"
    WORK_ROOT = "work"

    BRANCH_DATA = "data"
    BRANCH_IMAGES = "images"
    BRANCH_QUICKTIME = "quicktime"

    BRANCH_EXCHANGE = "exchange"
    BRANCH_SCENE_FILES = "scene_files"
    BRANCH_WORKSPACE = "workspace"
    BRANCH_CACHES = "caches"

    def __init__(self, context_data, file_format=None):
        self.context = context_data
        self.file_format = file_format
        self.projects_root = Path(os.getenv("ORIGIN_PROJECTS_ROOT"))

    # ----------------------------
    # internal helpers
    # ----------------------------

    def _task_base(self) -> Path:
        return Path(*self.context.task_path_elements())

    def _user_work_dir(self) -> str:
        return f"{self.WORK_ROOT}_{Users().curr_user()}"

    def _file_parent_dir(self) -> str | None:
        if not self.file_format:
            return None
        component = get_file_component_class(self.file_format)()
        return component.label

    def _asset_naming(self) -> AssetNaming:
        return AssetNaming(
            category=self.context.category,
            entity=self.context.entity,
            asset=self.context.asset_doc.name,
            asset_type=self.context.asset_doc.type,
            version=self.context.next_version(),
        )

    # ----------------------------
    # base roots
    # ----------------------------

    def publish_root(self) -> Path:
        return self._task_base() / self.PUBLISH_ROOT

    def work_root(self) -> Path:
        return self._task_base() / self._user_work_dir()

    # ----------------------------
    # publish paths
    # ----------------------------

    def publish_path(self, branch: str, create=False) -> Path:
        naming = self._asset_naming()

        path = (
            self.publish_root()
            / branch
            / naming.asset_dir
            / naming.version_dir
        )

        parent = self._file_parent_dir()
        if parent:
            path /= parent

        return self._finalize(path, create)

    # ----------------------------
    # work paths
    # ----------------------------

    def work_path(self, branch: str | None = None, create=False) -> Path:
        path = self.work_root()
        if branch:
            path /= branch
        return self._finalize(path, create)

    def create_work_folders(self):
        for branch in (
            self.BRANCH_CACHES,
            self.BRANCH_EXCHANGE,
            self.BRANCH_SCENE_FILES,
            self.BRANCH_WORKSPACE,
        ):
            self.work_path(branch, create=True)

    # ----------------------------
    # resolution helpers
    # ----------------------------

    def _finalize(self, relative_path: Path, create: bool) -> Path:
        absolute = self.projects_root / relative_path
        if create:
            absolute.mkdir(parents=True, exist_ok=True)
        return absolute

    def to_relative(self, path: Path) -> Path:
        return path.relative_to(self.projects_root)

    def to_unix(self, path: Path) -> str:
        return path.resolve().as_posix()

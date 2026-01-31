from dataclasses import dataclass


@dataclass(frozen=True)
class AssetNaming:
    category: str
    entity: str
    asset: str
    asset_type: str
    version: str

    @property
    def file_name(self) -> str:
        return "__".join([self.category, self.entity, self.asset, self.version])

    @property
    def asset_dir(self) -> str:
        return "__".join([self.asset_type, self.entity, self.asset])

    @property
    def version_dir(self) -> str:
        return "__".join([self.category, self.entity, self.asset, self.version])
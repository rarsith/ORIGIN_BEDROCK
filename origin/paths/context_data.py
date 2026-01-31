from dataclasses import dataclass
from origin.envars.origin_envars import ContextHandler


@dataclass(frozen=True)
class OriginContextData:
    context: ContextHandler
    category: str
    entity: str
    asset_doc: object

    @classmethod
    def from_context(cls, context: ContextHandler | dict):
        if isinstance(context, dict):
            ctx = ContextHandler()
            ctx.load_session(context)
        else:
            ctx = context

        return cls(
            context=ctx,
            category=ctx.get_entity_category(),
            entity=ctx.entity_name,
            asset_doc=ctx.database_handler().get_db_asset_document(),
        )

    def task_path_elements(self) -> list[str]:
        return self.context.resolve_to_task_type_context().split(".")

    def next_version(self) -> str:
        version, _ = self.asset_doc.operations().get_next_version()
        return version
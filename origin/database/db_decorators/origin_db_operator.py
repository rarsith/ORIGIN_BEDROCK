from origin.database import ProjectCollections


def origin_db_operation(db_path):
    def origin_doc_attribute(func):
        def wrapper(self, value=None):
            if value is None:
                value = func(self)

            method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                            entry_id=self.entity_id,
                                            attribute=db_path), self.db_operation)

            if value is not None:
                return method(value)
            else:
                result = method()
                return result
        return wrapper
    return origin_doc_attribute

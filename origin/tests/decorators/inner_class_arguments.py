from o_database.mongo import DBFind, DBSet
from o_database.collections.connections import ProjectCollections
from o_database.entities.attributes_paths import DbEntityAttrPath


# Define a decorator function that accepts arguments


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

# Define a class
class MyClass:
    def __init__(self, operation, db_operation, entity_id=None):
        self.entity_id = entity_id
        self.operation = operation
        self.db_operation = db_operation
        self.class_variable = "Hello"

    @origin_db_operation(db_path=DbEntityAttrPath().to_type())
    def get_entity_type(self):
        pass

    @origin_db_operation(db_path=DbEntityAttrPath().to_type())
    def set_entity_type(self, value=None):
        pass

    @origin_db_operation(db_path=DbEntityAttrPath().to_entity_name())
    def entity_name(self):
        pass


if __name__ == "__main__":
    from origin.envars import OriginEnvar

    path = ["assets", "characters"]
    OriginEnvar.show_name = "New_Era"
    OriginEnvar.origin_path_hierarchy = path
    OriginEnvar.entry_name = "hulk"
    asset_id = OriginEnvar.resolve_entity_id()

    setter_class = MyClass(operation=DBSet, db_operation="attribute_value", entity_id=asset_id)
    getter_class = MyClass(operation=DBFind, db_operation="attr_values", entity_id=asset_id)

    setter_class.set_entity_type(value="vechicle")
    ent_type = getter_class.get_entity_type()
    # obj.entity_type = "test"
    # ent_name = obj.entity_name()
    print(ent_type)
    # print(ent_name)
    # print(obj.entity_type)

    # Call the decorated method
    # result = obj.my_method(3, 4)
    # print("Result:", result)




    # def operations(orig_func):
    #     def wrapper():
    #         return orig_func()
    #
    #     return wrapper
    #     # method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
    #     #                                 entry_id=self.entity_id,
    #     #                                 attribute=attribute_name), self.db_operation)
    #     # print(method)
    #     # if value:
    #     #     method(value)
    #     # else:
    #     #     return method()


    # def create_op_inst(self, attribute_path, value=None):
    #     method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
    #                                     entry_id=self.entity_id,
    #                                     attribute=attribute_path), self.db_operation)
    #
    #     if value:
    #         method(value)
    #     else:
    #         return method()
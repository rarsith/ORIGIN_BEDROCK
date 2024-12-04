import inspect
from origin.database.entities import operators as ops
from origin.database.entities.operators import DBAsset


class ModelRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, model_class):
        self._registry[model_class.__name__] = model_class()

    def get_all_types(self):
        all_types = []
        for k, v, in self._registry.items():
            all_types.append(v.type)
        return all_types


# Instantiate the registry
registry = ModelRegistry()

for _, obj in inspect.getmembers(ops, inspect.isclass):
    if issubclass(obj, DBAsset) and obj != DBAsset:
        registry.register(obj)


if __name__ == "__main__":
    print(registry.get_all_types())
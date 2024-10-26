def get_entity_root_structure(dictionary):
    for keys, val in dictionary.items():
        yield keys


def deep_values(key, dictionary):
    if isinstance(dictionary, dict):
        for category, val in dictionary.items():
            if category == key:
                yield val
            elif isinstance(val, dict):
                for result in deep_values(key, val):
                    yield result
            elif isinstance(val, list):
                for d in val:
                    for result in deep_values(key, d):
                        yield result



# def get_deep_value(data: dict, path_list: list) -> dict:
#     """ @data: takes a nested dictionary
#         @path_list: takes a list or a single string
#         @returns: the value that is corresponding to the last list element in the path_list"""
#
#     if isinstance(path_list, str):
#         result = data.get(path_list)
#         return result
#     elif isinstance(path_list, list) and len(path_list) == 1:
#         result = data.get(path_list[0])
#         return result
#     else:
#         for index, entity in enumerate(path_list):
#             if isinstance(path_list, list) and len(path_list) > 1:
#                 level = data.get(entity)
#                 path_list.pop(index)
#                 return get_deep_value(level, path_list)

if __name__ =="__main__":

    key = "characters"

    dictionary_target = {"structure": {"sequences": {"type": "shots"}, "assets": {"type": "build", "characters": ["dudu","dada","kookoo"], "environments": ["env001","env002","env003"],"props": []}}}
    # print (dictionary_target.keys())

    deep_val = deep_values(key, dictionary_target)
    for item in deep_val:
        print (item)




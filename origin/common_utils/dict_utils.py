def is_subset_dict(subset, main):
    if not isinstance(subset, dict) or not isinstance(main, dict):
        return subset != main

    for key, value in subset.items():
        print(key, value)
        if key not in main:
            return True
        if is_subset_dict(value, main[key]):
            return True
    return False


def merge_dicts(dictA, dictB):
    for key, value in dictB.items():
        if key in dictA and isinstance(dictA[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            merge_dicts(dictA[key], value)
        else:
            # Otherwise, overwrite dictA's value with dictB's value
            dictA[key] = value
    return dictA

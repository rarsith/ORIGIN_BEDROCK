import re

def write_nice_names(items_list):
    extract = []
    for each in items_list:
        catch_it = re.sub('_', ' ', each)
        extract.append(catch_it.title())
    return extract

def write_ugly_names(items):
    if isinstance(items, str):
        return items.lower().replace(" ", "_")
    elif isinstance(items, list):
        extract = [item.lower().replace(" ", "_") for item in items]
        return extract


import re

def write_nice_names(items_list):
    extract = []
    for each in items_list:
        catch_it = re.sub('[_]', ' ', each)
        extract.append(catch_it.title())
    return extract
def make_path(*data, **kwargs):
    clean_data = []
    if data or data is not None:
        for element in data:
            if isinstance(element, str):
                clean_data.append(element)
        dotted_path = str(".".join(clean_data))
        return dotted_path
    return kwargs





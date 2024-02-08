def string_to_list(data, splitter="."):
    """ @data: takes in string with OR without a separator (".", "_"...)
        @splitter: default splitter used
        @returns: if multiple resulting splits -> a list,
                  else-> the initial @data value """

    if not splitter in data:
        return data
    get_path_entities = data.split(splitter)
    return get_path_entities
def remove_first_level(nested_dict:dict) ->dict:
    """ A function that removes the first level of a nested dictionary:

    Args:
        nested_dict (dict): a nested dictionary

    Returns:
        dict: dictionary with first level removed
    """
    result = {}
    for outer_key, outer_value in nested_dict.items():
        if isinstance(outer_value, dict):
            result.update(outer_value)
        else:
            result[outer_key] = outer_value
    return result

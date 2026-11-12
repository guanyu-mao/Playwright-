def invert_nested_dict(nested_dict: dict) -> dict:
    """This function will:
    * Handle nested dictionaries of arbitrary depth
    * Preserve empty dictionaries in the inverted result
    * Use tuples as keys for the inverted nested structure

    Args:
        nested_dict (dict): a nested dictionary

    Returns:
        dict: an inverted nested dictionary
    """
    inverted = {}

    def invert(d, parent_keys=()):
        for k, v in d.items():
            new_key = parent_keys + (k,)
            if isinstance(v, dict):
                if v:  # If the nested dictionary is not empty
                    invert(v, new_key)
                else:
                    inverted[new_key] = {}
            else:
                inverted[v] = new_key

    invert(nested_dict)
    return inverted

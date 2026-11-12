def var_exits(var:str)->bool:
    """for checking existence in globals() function

    Args:
        var (str): variable name

    Returns:
        bool: `True` or `False`
    """
    if var in globals():
        return True
    else:
        return False

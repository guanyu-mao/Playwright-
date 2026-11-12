def check_filter_menu_open(page) -> bool:
    """ Check if a filter menu is opened

    Args:
        page (playwright.sync_api._generated.Page): page context

    Returns:
        bool: Return `True` if there is an opened menu otherwise `False`
    """
    # check if filter menu is opened
    element = page.locator('div.qmenu.dropdown-menu.search-menu.positioned')
    if element.count()>0:
        # close the menu first
        return True
    else:
        return False

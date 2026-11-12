import src.scraper_functions as scp

def open_filter_menu(page,filter_text:str):
    """This function selects a desired filter menu.

    It intelligently checks if the filter menu is already opened and closes it before opening one.

    Args:
        page (playwright.sync_api._generated.Page): page context
        filter_text (_type_): the short name of the filter. For a list of available filters run get_full_filter_text().

    Returns:
        page (playwright.sync_api._generated.Page): modified page
    """
    # click on the appropriate filter

    # make sure that the filter is closed before proceeding
    open = scp.check_filter_menu_open(page)

    # if menu is opened close it first
    if open:
        page = scp.click_away(page)

    text = scp.get_full_filter_text(filter_text)

    try:
        page.get_by_role('button', name=text).click()
    except:
        # if fail to load click on the page again
        page.get_by_role('button', name=text).click()

    # wait for the options menu to fully load
    state = scp.wait_options_loaded(page)

    if state == False:
        msg = 'Option for '+text+' could not fully load'
        print(msg)
        scp.write_to_log(msg)

    return page

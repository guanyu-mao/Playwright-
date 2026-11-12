import src.scraper_functions as scp
def click_away(page):
    """ Click on a page. Used to close an opened menu

    Args:
        page (playwright.sync_api._generated.Page): page context
    Returns:
        page (playwright.sync_api._generated.Page): modified page
    """
    page.mouse.click(300, 200)

    # wait for the menu to close before returning the page
    page = scp.wait_menu_close(page)

    return page

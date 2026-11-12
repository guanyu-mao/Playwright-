import time
def wait_menu_close(page, timeout = 30):
    """ Wait for the filter menu to close before proceeding

    Args:
        page (playwright.sync_api._generated.Page): page context
        timeout (int): timeout before exiting this menu. Avoids infinite loops

    Returns:
        playwright.sync_api._generated.Page: page context
    """
    # wait for menu to close
    start_time = time.time()

    while True:
        if page.locator('div.dropdown-menu').is_visible():
            # wait 1 sec
            page.wait_for_timeout(1000)  # Adjust the wait time as needed
        elif page.locator('div.dropdown-menu').is_hidden():
            page.wait_for_timeout(1000)  # Adjust the wait time as needed
            return page
        else:
            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                return page
            # Wait for a short period before checking again
            page.wait_for_timeout(1000)
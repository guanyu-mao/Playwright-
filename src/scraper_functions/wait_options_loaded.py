import time

def wait_options_loaded(page, timeout = 30):
    """ Wait for options in the filter menu to load

    Args:
        page (playwright.sync_api._generated.Page): page context
        timeout (int, optional): Timeout before proceeding with an error message. Defaults to 30 seconds.

    Returns:
        bool: True or false
    """
    locator = page.locator('li[role="option"]')
    start_time = time.time()

    while True:
        # Wait for the potential changes to take effect
        page.wait_for_timeout(1000)

        if locator.count()>0:
            # we have more than 0 elements loaded then exit
            return True

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            return False

        # Wait for a short period before checking again
        page.wait_for_timeout(1000)

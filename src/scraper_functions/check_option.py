import time
import src.scraper_functions as scp

def check_option(page,filter_name:str, filter_option:str, timeout = 30):
    """ Check if an option was selected correctly

    Args:
        page (playwright.sync_api._generated.Page): page context
        filter_name (str): name of the filter option to be selected
        filter_option (str): filter option from the menu selected.
        timeout (int, optional): Timeout before creating a warning this action. Defaults to 30 seconds.

    Returns:
        bool: True or false
    """

    start_time = time.time()

    text = scp.get_full_filter_text(filter_name)

    while True:
        # Wait for the potential changes to take effect
        page.wait_for_timeout(1000)  # Adjust the timeout as needed

        # locate the filter text and select the active text only
        # This will fail if multiple filters are enabled!
        locator = page.locator('span.summary.ng-binding.active-filtering')

        # extract the filter text
        live_text = locator.text_content().strip()

        # get the expected text
        expected_text = scp.get_full_filter_text(filter_name)

        # compare that to expected text
        # Check if the table content has changed
        if live_text != expected_text:
            return True

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            return False

        # Wait for a short period before checking again
        # Adjust the wait time as needed
        page.wait_for_timeout(1000)

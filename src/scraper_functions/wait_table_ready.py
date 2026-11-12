import io
import pandas as pd
import time
import src.scraper_functions as scp

def wait_table_ready(page,old_table:str, timeout = 30):
    """ Wait for table to update before doing something with it. Either wait for a spinner or look for changes in the table

    Args:
        page (playwright.sync_api._generated.Page): page context
        old_table (str): initial table used for comparison
        timeout (int, optional): Timeout before cancelling this action. Defaults to 30 seconds.

    Returns:
        bool: True or false
    """

    old_table_io = io.StringIO(old_table)
    old_table_pd = pd.read_html(old_table_io)[0]

    # If no spinner appeared then lets do something else
    # Wait for the loading spinner to disappear
    start_time = time.time()

    while True:
        # Wait for the potential changes to take effect
        page.wait_for_timeout(1000)  # Adjust the timeout as needed

        # Capture the new state of the table
        new_table = scp.get_table(page)
        new_table_io = io.StringIO(new_table)
        new_table_pd = pd.read_html(new_table_io)[0]

        # Check if the table content has changed
        if not new_table_pd.equals(old_table_pd):
            # if it has, break the loop and return true
            return True

        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            # if it has return false since the above condition was never satisfied
            return False

        # Wait for a short period before checking again
        page.wait_for_timeout(1000)  # Adjust the wait time as needed

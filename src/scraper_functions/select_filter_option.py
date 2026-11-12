import warnings

def select_filter_option(page,option_id:str,retries:int = 1,timeout:int = 10000 ):
    """Select a filter option.

    If an option is already selected, instead

    Args:
        page (playwright.sync_api._generated.Page): page context
        option_id (str): The option css id.
        retries (int): number of retries to do after not finding the element on the page. Could be because the element has not fully loaded yet.
        timeout (int): how long to wait before retrying

    Returns:
        page (playwright.sync_api._generated.Page): modified page
    """
    # assuming a filter menu is already opened fully loaded

    # check that the option is visible (in one of the menu items)
    # if the option is not visible then fail (error in the input file)
    # check that the option is selectable (enabled)
    # if its there but not selectable then skip the selection
    while retries > 0:
        if page.locator('li[id="'+option_id + '"]').is_visible():
            if page.locator('li[id="'+option_id + '"]').is_enabled():
                page.locator('li[id="'+option_id + '"]').click()
                break # Exit the loop after clicking the element
            else:
                warnings.warn('The element '+ page.locator('#'+option_id).text_content().strip() + ' with options_id '+option_id + ' is not enabled. Skipping.')
                break # Exit the loop after handling the warning
        else:
            warnings.warn('The element '+ page.locator('#'+option_id).text_content().strip() + ' with options_id '+option_id + ' is not visible. Retrying.')
            page.wait_for_load_state(timeout=timeout)
            retries -= 1
            if retries > 0:
                continue  # Go back to the beginning of the loop and retry
            else:
                raise Exception('The element '+ page.locator('#'+option_id).text_content().strip() + ' with options_id '+option_id + ' is not visible. Are you sure you correctly defined your input file? Failing.')
    return(page)

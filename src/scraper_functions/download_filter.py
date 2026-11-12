import src.scraper_functions as scp

def download_filter(page,org_short_name:str,download_location:str):
    """ Loop through all available filters on the dashboard and download each filter option

    Args:
        page (playwright.sync_api._generated.Page): page context
        org_short_name (str): organization's short name
        download_location (str): Where to save the downloaded files

    Returns:
        _type_: _description_
    """

    # check if the resets button is showing then click it
    # TODO could reimplement this by using test_id instead of role for more consistency
    # data-testid="reset-filters-to-default-button"
    if page.get_by_role('button', name = "Reset to Default").is_visible():
        page.get_by_role('button', name = "Reset to Default").click()

    # get all available filters
    available_filters = scp.get_full_filter_text(filter_short_text='DICTIONARY')

    # iterate over each filter, download each table and save it to disk
    for k,v in available_filters.items():
        scp.download_filter_option(page = page,org_short_name = org_short_name,download_location = download_location, filter_name= k)

    return page

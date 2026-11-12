import src.scraper_functions as scp

def get_filter_option_css(page,filter_value:str,filter_name:str) -> str:
    """ Get the current filter option's css id. This is used to select a specific option rather than selecting it by text.
    Args:
        page (playwright.sync_api._generated.Page): page object
        filter_value (str): filter value to select the css value for (e.g., "manager")
        filter_name (str): filter category to use (e.g., "employment_group")

    Returns:
        str: css string value
    """
    # filter_option_text_full = scp.get_short_filter_description("manager",direction = "full to short")
    filter_option_text_full = scp.get_short_filter_description(filter_value,direction = "full to short")

    # get list of filter options
    # filter_options = scp.get_download_options(page,"employment_group")
    filter_options = scp.get_download_options(page,filter_name)

    filter_options_no_category = scp.remove_first_level(filter_options)
    filter_options_no_category_inverted = scp.invert_nested_dict(filter_options_no_category)

    # locate the css_id for the filter_filter_value we have in our scenario
    css_id = filter_options_no_category_inverted[filter_option_text_full]
    return css_id[0]

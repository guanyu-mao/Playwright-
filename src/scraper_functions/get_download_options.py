
import warnings
import src.scraper_functions as scp

def get_download_options(page,filter_text:str):
    """ Get available download options for a filter

    Args:
        page (playwright.sync_api._generated.Page): page object
        filter_text (str): A short filter name (e.g., 'region' for 'Region: All')

    Returns:
        dict: Dictionary of available options
    """
    # Check if the filter menu is open and close if necessary
    open = scp.check_filter_menu_open(page)
    if open:
        page = scp.click_away(page)

    # select the correct filter
    page = scp.open_filter_menu(page,filter_text)

    # close the filter and reopen it again.
    # This is a fix for #11. For some reason the first time a filter opens it is not always correct
    # Check if the filter menu is open and close if necessary
    open = scp.check_filter_menu_open(page)
    if open:
        page = scp.click_away(page)

    page.wait_for_timeout(1000)

    # select the correct filter
    page = scp.open_filter_menu(page,filter_text)
    # Once the menu opens wait for 2 seconds before proceeding to make sure everything is fully loaded
    # TODO #14
    page.wait_for_timeout(2000)

    # if full data has been loaded
    try:
        # wait for the selectors to fully load
        page.wait_for_selector('#sub0 > ul:nth-child(1) > li[role="option"]')

    except Exception as e:
        # not everything was loaded fully. Need to:
        # write a log
        # show a warning
        warnings.warn('Could not load the contents of '+filter + 'filter. Log written to logs.txt')
        scp.write_to_log(msg='Count load contents of the '+filter)

        all_options_dict = { }
        anonymity_options_dict = { }
        no_data_dict = { }
        return {'individual':all_options_dict,'grouped':anonymity_options_dict,'nodata':no_data_dict}

    else:
        # there was no error. Continue on

        # get the available options for each category

        # grab all sections
        sections = page.query_selector_all('#sub0 > ul[role=group]')

        # a dictionary of the form {'sub0_2':'Central region'}
        all_options_dict = { }
        anonymity_options_dict = { }
        no_data_dict = { }

        # iterate over each section
        for index,section in enumerate(sections):
            if index == 0:
                # Section 1: All individual options
                # option 1 does not have a title so I need to use this special index when accessing it
                # always exists because the `All` option is always visible
                section_title = 'individual'

                # get all available options for the section
                options = section.query_selector_all('li[role="option"]')
                for x in options:
                    option_text = x.text_content().strip()
                    option_id = x.get_property('id').json_value()
                    all_options_dict.update({option_id: option_text})
            else:
                # get the title of the section
                section_title = section.query_selector_all('li[role="presentation"]')[0].text_content().strip()

                # get all available options for the section
                options = section.query_selector_all('li[role="option"]')

                for x in options:
                    option_text = x.text_content().strip()
                    option_id = x.get_property('id').json_value()
                    # sometimes there might not be any 2nd and 3rd sections. To fix issue #8 we check that the correct section title matches
                    if section_title == 'Grouped for Anonymity':
                        # section 2 found and is the anonymity section
                        # update the anonymity_options_dict with appropriate vars
                        anonymity_options_dict.update({option_id: option_text})
                    elif section_title == 'No Data Found':
                        # anonymity section missing so we have the `No Data Found` section instead
                        # substitute it with no_data instead
                        no_data_dict.update({option_id: option_text})
                    else:
                        warnings.warn('Section 3: of the '+filter_text+' filter was expected to be "No Data found" but instead it was '+ section_title + ' there some extra data in this section. You should investigate.')
        # without selecting an option click away
        page.mouse.click(300, 200)

        # return an dictionary of options gathered
        return {'individual':all_options_dict,'grouped':anonymity_options_dict,'nodata':no_data_dict}

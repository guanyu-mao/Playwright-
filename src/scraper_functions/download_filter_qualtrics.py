import src.scraper_functions as scp

def download_filter_qualtrics(page,filter_name:str,download_location:str,org_short_name:str):
    """ Download all data from a specified `filter_name` using Qualtrics's built in download functionality (3 dots menu next to the table)

    Args:
        page (playwright.sync_api._generated.Page): page context
        filter_name (str): short filter name. For available options use the key in get_full_filter_text()
        download_location (str): Download location on the disk
        org_short_name (str): short organizational name. Used in the filename when storing the data.
    """

    # a dictionary of the form {'individual': {'sub0_2':'Central region'}}
    filter_options = scp.get_download_options(page,filter_name)

    # download the individual data for individual options
    options = filter_options['individual']
    if len(options)>0:
        for k,v in options.items():
            if v =='All':
                # skip downloading this one (we already did it initially)
                pass
            else:
                # check that the filter is closed before proceeding
                open = scp.check_filter_menu_open(page)

                # if menu is opened close it first
                if open:
                    page = scp.click_away(page)

                # select the filter menu
                page = scp.open_filter_menu(page,filter_name)

                # create a short name to be used when saving the file
                filter_value_short = scp.get_short_filter_description(v)

                # get the id of when I need to click on
                id = k

                # select the correct filter option
                page = scp.select_filter_option(page,id)

                # click away
                page = scp.click_away(page)

                page = scp.select_moe_statements(page)

                # wait for 3 sec
                # TODO #14
                page.wait_for_timeout(3000)

                # download the data
                scp.download_filter_qualtrics_selected(page,download_location,org_short_name,filter_name,filter_value_short)

                # deselect the filter option
                # select the filter menu
                page = scp.open_filter_menu(page,filter_name)

                # select the correct filter option
                page = scp.select_filter_option(page,id)

                # click away
                page = scp.click_away(page)

import src.scraper_functions as scp
from typing import Optional

def save_table(page,
               type:str ,
               filter_name:str,
               filter_description:str,
               download_location:str,
               org_short_name:str,
               download_id:Optional[str] = None,
               filter_value_filename: Optional[str] = None):
    """ Perform a standard set of actions before saving the table. This ensures that the table is correctly saved. Its a wrapper function around the `save_table_data()` function.

    Args:
        page (playwright.sync_api._generated.Page): page context
        type (str): Table type to save. There are two type: `data` and `nodata`. For `nodata` tables we use the existing table and replace all filled items with zero. No data verification if performed.
        filter_name (str): filter category selected (e.g. `region`)
        filter_description (str): filter option from the filter category selected (e.g., `Central Region`)
        download_location (str): where on the disk to save the file (use full path names)
        org_short_name (str): organization name used when saving the file. Use short description (e.g., `bipd`).
        download_id (str): download filter id (e.g., `sub0_02`). If `type='nodata` then this parameters is optional (set to None).
        filter_value_filename (Optional[str]):Optional file name used when using multiple filters (e.g., when downloading data grouped for anonymity)
    """

    # check that the filter is closed before proceeding
    open = scp.check_filter_menu_open(page)

    # if menu is opened close it first
    if open:
        page = scp.click_away(page)

    if type == 'data':

        # get the current table state
        old_table = scp.get_table(page)

        # select the filter menu
        page = scp.open_filter_menu(page,filter_name)

        # select the correct filter option
        page = scp.select_filter_option(page,download_id)

        # click away
        page = scp.click_away(page)

        # wait for the table to change:
        state = scp.wait_table_ready(page,old_table=old_table)

        if state == False:
            msg = 'Option for '+ filter_name+': '+ filter_description +' could not fully load'
            print(msg)
            scp.write_to_log(msg)

        # check that the correct option is selected on the page
        state = scp.check_option(page,
                    filter_name=filter_name, filter_option = filter_description)

        if state == False:
            msg = 'Variable '+ filter_name+': '+ filter_description +' was not correctly selected by (select_filter_option()). Data incorrectly saved'
            print(msg)
            scp.write_to_log(msg)

        # download the data
        scp.save_table_data(
            page,
            org_short_name = org_short_name,
            download_location =  download_location,
            filter_name = filter_name,
            filter_value_short = filter_description,
            fill_with_nulls = False,
            filter_value_filename = filter_value_filename
            )

        # deselect the filter option and return to default state (Filter: All)
        # select the filter menu
        page = scp.open_filter_menu(page,filter_name)

        # select the correct filter option
        page = scp.select_filter_option(page,download_id)

        # click away
        page = scp.click_away(page)

    else:
        # don't do any verification just save the table that is shown on the page
        scp.save_table_data(
            page,
            org_short_name = org_short_name,
            download_location =  download_location,
            filter_name = filter_name,
            filter_value_short = filter_description,
            fill_with_nulls = True,
            filter_value_filename = filter_value_filename
            )

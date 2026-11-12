from dotenv import load_dotenv
import os
import src.scraper_functions as scp

def save_table_manually(
        page,
        download_location: str = None,
        org_name:str | list = None):
    """A wrapper function around `save_table_data()` to allow for manually downloading the selected filter options from the chrome browser

    Args:
        page (playwright.sync_api._generated.Page): page context
        download_location (str): where on the disk to save the file (use full path names). Defaults to None which means download location is taken from the environment variable 'download_location'.
        org_name (str | list, optional): If using more than two orgs, allow for specification of the org name rather than gather that from the webpage. Defaults to None.
    """
    # where to save files on your computer
    if download_location is None:
        # load configuration file (user, password, dashboard_url, download location)
        load_dotenv(override=True)
        download_location = os.getenv('download_location')

    # get the org name
    if org_name is None:
        org_description = page.get_by_role('button',name= "Results for: ").all_inner_texts()
        org_name_raw = [element.split(':')[1] for element in org_description]
        org_name = str(org_name_raw[0]).replace("\n","")
        org_short_name = scp.get_org(org_name)
    if isinstance(org_name,list):
        # we have multiple org names selected
        org_short_name="&".join(org_name)

    # Check if the menu is opened first and close it before preceding
    expanded = page.get_by_test_id("org-hierarchy-filter-button").get_attribute("aria-expanded")
    if expanded:
        page = scp.click_away(page)
    # see which filter were selected
    texts = page.get_by_role("toolbar").get_by_role("button").all_inner_texts()

    # now select only the filter names not the values
    # select only the elements that contain a non-default value of 'all'
    selected_filters = [element for element in texts if not element.endswith(' All ')]

    if len(selected_filters)>0:
        selected_filter_names = [element.split(':')[0] for element in selected_filters]

        # a list of filers that were selected
        filters = [scp.get_full_filter_text(description, direction="full to short") for description in selected_filter_names]

        # put the filter names into a filter_name so that it can be saved as the file name
        # concatenate multiple filters names with &
        filter_name = "&".join(filters)

        # for each filter check what items were checked, extract then concatenate them
        filter_value_short = []

        # close any open menus
        page = scp.click_away(page)

        for item in filters:
            page = scp.open_filter_menu(page,item)
            # close the filter and reopen it again.
            # This is a fix for #11. For some reason the first time a filter opens it is not always correct
            # Check if the filter menu is open and close if necessary
            open = scp.check_filter_menu_open(page)
            if open:
                page = scp.click_away(page)

            # TODO #14
            page.wait_for_timeout(1000)

            # select the correct filter again
            page = scp.open_filter_menu(page,item)

            # identify which values are selected in the filter menu
            # items in the `No Data Found`` group can be selected by are excluded from the count
            # items in the `Grouped for Anonymity` are selectable as well if selected before the restriction is applied and will show in the data
            # items in `Grouped for Anonymity` are not automatically selected! For details see: #25.
            selected_filter_values = page.get_by_role("listbox").get_by_role("option", selected=True).all_inner_texts()

            # check if there were any non-selected options that were groped for anonymity along along with selected options
            group_items = page.get_by_role("group")

            # initialize data not available
            nodata_options = [ ]

            group_count = group_items.count()
            titles = group_items.get_by_role("presentation").all_inner_texts()
            # first group is always the individual options
            group_title = ["All"]
            group_title = group_title + titles

            # group each of the menu options in the filter in the 3 possible groups of states
            # 1. individual variables
            # 2. variables grouped for anonymity
            # 3. variables without any data
            for i in range(0,group_count):
                group_values = group_items.nth(i).get_by_role("option").all_inner_texts()
                if group_title[i] == "No Data Found":
                        nodata_options = group_values

            # Observation: the options that are grouped have a css id that is higher than the <li> id of the locator with text Grouped for Anonymity

            # check if our selected items are in either the anonymity or nodata list we just constructed.
            items_in_nodata_group_to_remove = []
            for val in selected_filter_values:
                # if in nodata option list
                # then remove the option from our filter list since there is not data for that one
                if val in nodata_options:
                    items_in_nodata_group_to_remove.append(val)

            # remove all selected options that dont have data elements (they cannot be downloaded)
            # I am unsure if I need this since, technically I cannot select an option that cannot be downloaded
            for item in items_in_nodata_group_to_remove:
                selected_filter_values.remove(item)

            # convert the selected filter values to their short names
            text_filter_values = [ scp.get_short_filter_description(value) for value in selected_filter_values ]
            filter_value_short.append(";".join(text_filter_values))
        # concatenate multiple filters options with &
        filter_value_short = "&".join(filter_value_short)

    # save table data
    else:
        filter_name="all"
        filter_value_short="all"
    scp.save_table_data(page,
                    org_short_name=org_short_name,
                    download_location=download_location,
                    filter_name=filter_name,
                    filter_value_short=filter_value_short,
                    fill_with_nulls=False,
                    filter_value_filename=None
                    )
    page = scp.click_away(page)

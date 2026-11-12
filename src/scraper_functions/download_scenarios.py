import src.scraper_functions as scp

def download_scenarios(page, file_name:str):
    """ Download scenarios defined in a file

    Args:
        page (playwright.sync_api._generated.Page): page object
        file_name (str): file name to use to load scenarios from. The yaml file is is stored in "./data/scenarios/name.yml"
    """
    # get the scenario to use
    # e.g., all_scenarios = scp.load_download_scenarios("ardi.yml")
    all_scenarios = scp.load_download_scenarios(file_name=file_name)

    # Reset the current filters
    page = scp.reset_filter_values(page)

    # Iterate over all dictionaries and their values
    counter = 1
    for scenario_name, scenario_spec in all_scenarios.items():
        print("Downloading scenario: "+scenario_name+". Number "+ str(counter) + " of " + str(len(all_scenarios)))
        counter = counter+1
        # print(f"{scenario_name}:")
        for filter_name, filter_value in scenario_spec.items():
            #print(f"  {filter_name}: {filter_value}")

            print("Selecting filter name: "+filter_name)

            # if we have a list a values we need to make multiple selections
            if type(filter_value) == list:
                for list_item in filter_value:
                    css_id = scp.get_filter_option_css(page,filter_value=list_item,filter_name = filter_name)
                    page = scp.open_filter_menu(page,filter_text=filter_name)

                    print("Selecting filter value: "+list_item+" with css_id: "+css_id)
                    scp.select_filter_option(page,css_id)
                    page = scp.click_away(page)
            else:
                css_id = scp.get_filter_option_css(page,filter_value=filter_value,filter_name = filter_name)
                page = scp.open_filter_menu(page,filter_text=filter_name)

                print("Selecting filter value: "+filter_value+" with css_id: "+css_id)
                scp.select_filter_option(page,css_id)
                page = scp.click_away(page)

        # save table and move to the next scenario
        scp.save_table_manually(page)
        page = scp.reset_filter_values(page)

    print("Finished downloading scenario: "+file_name)

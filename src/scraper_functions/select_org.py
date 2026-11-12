import src.scraper_functions as scp

def select_org(page,org_name:str | list,orgs:dict = None):
    """ Select the given org in the initial filter page

    Args:
        page (playwright.sync_api._generated.Page): page context
        org_name (str | list): which organizations should be selected (use the short name - e.g., bipd for Business Intelligence & Practice Division)
        orgs (Optional[dict]): option orgs dictionary containing the orgs list
    Returns:
        page: return modified page object
    """
    # reset current org selection
    # open org selection menu
    page.get_by_role('button',name= "Results for: ").click()

    # reset the org if one is selected
    if page.get_by_role('button', name = 'Reset').is_visible():
        page.get_by_role('button', name = 'Reset').click()

    if isinstance(org_name,str):
        # find the full org name
        org_name = scp.get_org(org_name,orgs)

        # Check if the menu is opened first and close it before preceding
        expanded = page.get_by_test_id("org-hierarchy-filter-button").get_attribute("aria-expanded")
        if expanded:
            page = scp.click_away(page)
        # open org selection menu
        page.get_by_role('button',name= "Results for: ").click()

        # reset the org if one is selected
        if page.get_by_test_id('reset-footer-reset').is_visible():
            page.get_by_test_id('reset-footer-reset').click()

        if org_name == "Ontario Public Service":
            # for ops data simply select the reset button
            page.get_by_test_id('reset-footer-reset').click()
        else:
            print("Selecting "+org_name)
            page.fill('input[id="quick-search-list"]', org_name)
            page.get_by_role('menuitem').nth(0).click()

        # wait for 7 sec
        # TODO #14
        page.wait_for_timeout(7000)

        page = scp.click_away(page)

    if isinstance(org_name,list):
        # we have multiple orgs so select  each one one by one
        for org in org_name:
            print("Selecting "+org)
            org_name = scp.get_org(org,orgs)
            # Check if the menu is opened first and close it before preceding
            expanded = page.get_by_test_id("org-hierarchy-filter-button").get_attribute("aria-expanded")
            if expanded:
                page = scp.click_away(page)

            # open org selection menu
            page.get_by_role('button',name= "Results for: ").click()

            if org_name == "Ontario Public Service":
                # for ops data produce an error message
                # TODO #23 Check that Org selection is mutually exclusive (you cannot select a sub-org and and org together)
                raise ValueError('You cannot select Ontario Public Service when selecting multiple orgs. Orgs selection must be mutually exclusive.  Aborting')
            else:
                page.fill('input[id="quick-search-list"]', org_name)
                page.get_by_role('menuitem').nth(0).click()

            # wait for 4 sec
            # TODO #14
            page.wait_for_timeout(4000)

            page = scp.click_away(page)

    return page

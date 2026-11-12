
def fetch_documents(page) -> None:
    """ Fetch Documents on Lucid Home Page

    Args:
        page (playwright.sync_api._generated.Page): page context
        user (str): login user name
        password (str): login user password
        login_url (str): URL to use for login
        dashboard_url (str): Redirect to this URL after a successful login
    """

    # Click on document Tab
    page.pause()
    page.locator("[id=\"_weave_e_271\"] iframe").content_frame.get_by_label("AccumulatedCosts").locator("div").filter(has_text="AccumulatedCosts VIEW").first.click()

    print('filter worked')

    page.pause()
    #get the iframe's content frame
    frame = page.locator('[id="_weave_e_271"] iframe').first.content_frame()
    options = frame.get_by_role("option")



    return page

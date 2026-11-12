def go_to_page(page) -> None:
    """ Open the Qualtrics login page and log me in

    Args:
        page (playwright.sync_api._generated.Page): page context
        user (str): login user name
        password (str): login user password
        login_url (str): URL to use for login
        dashboard_url (str): Redirect to this URL after a successful login
    """
    # Navigate to the login page
    target_url = "https://portal.azure.com/#@Ontariogov.onmicrosoft.com/resource/subscriptions/d491ccef-9bda-4adf-a63e-cbfc63d9b368/resourceGroups/azr-prd-mx-0604-wrk-cc-rgp-bipdde-0000-prod/costanalysis"
    page.goto(target_url)
    
    print('finished landing the page')



    return page

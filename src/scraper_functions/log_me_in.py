def log_me_in(page, user: str, password: str, login_url: str, dashboard_url: str):
    """Automate Microsoft/Azure login."""
    page.goto(login_url)

    # Wait for either the email input or dashboard to appear
    try:
        # Try to find the email input (Microsoft uses name="loginfmt")
        page.wait_for_selector('input[name="loginfmt"]', timeout=10000)
        page.fill('input[name="loginfmt"]', user)
        page.click('input[type="submit"], button[type="submit"]')

        # Wait for password input and fill it
        page.wait_for_selector('input[type="password"]', timeout=10000)
        page.fill('input[type="password"]', password)
        page.click('input[type="submit"], button[type="submit"]')

        # Optionally handle "Stay signed in?" prompt
        try:
            page.wait_for_selector('input[id="idBtn_Back"]', timeout=5000)
            page.click('input[id="idBtn_Back"]')
        except:
            pass  # If not present, continue

        # Wait for dashboard/home to load
        page.wait_for_url(dashboard_url, timeout=60000)
        print('Login successful')
    except Exception as e:
        print("Login fields not found, you may already be logged in or the page layout has changed.")
        # Optionally, wait for dashboard just in case
        page.wait_for_url(dashboard_url, timeout=60000)
    return page
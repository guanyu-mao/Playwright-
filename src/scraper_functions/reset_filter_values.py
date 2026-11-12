from playwright.sync_api import expect

def reset_filter_values(page):
    """Reset the current filter selection

    Args:
        page (playwright.sync_api._generated.Page): page object

    """
    if page.get_by_text('Reset to Default').is_visible():
        print("Resetting filters")
        page.get_by_text('Reset to Default').click()
    else:
        print("No filters to reset")

    # check that the filter has been reset
    expect(page.get_by_text('Reset to Default')).to_be_hidden(timeout=5_000)
    print("Filters are reset!")
    # TODO #14 - this delay can safely be removed
    # add 1s delay when resetting filters to ensure everything is back to initial settings
    page.wait_for_timeout(1000)

    return page

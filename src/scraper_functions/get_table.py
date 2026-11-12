def get_table(page):
    """ get first table with data

    Args:
        page (playwright.sync_api._generated.Page): page context

    Returns:
        str: full table in html
    """
    # select the new table (its always the first table)
    table_object = page.locator('table.simple-table.row-separators.col-separators').nth(0)

    table_html = table_object.inner_html()

    table_html_full = f'<table>{table_html}</table>'

    return table_html_full

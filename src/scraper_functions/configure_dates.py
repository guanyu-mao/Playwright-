import re

def configure_dates(page) -> None:
    """ Fetch Documents on Lucid Home Page

    Args:
        page (playwright.sync_api._generated.Page): page context
    """

    page.pause()
    page.frame_locator('[id="_weave_e_271"] iframe').locator("app-pill").filter(has_text="Jul").click()
    print("filter worked selecting the last month")

    page.pause()
    page.frame_locator('[id="_weave_e_271"] iframe').get_by_role("option", name="Last month Jun").click()

    # page.pause()
    # page.locator('[id="_weave_e_271"] iframe').get_by_role("button", name=re.compile(r"Granularity: Accumulated")).click()

    # page.pause()
    # page.locator('[id="_weave_e_271"] iframe').locator("#Daily").click()
    return page
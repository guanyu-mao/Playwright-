def download_filter_qualtrics_selected(page,download_location:str,org_short_name:str,filter_name:str,filter_selection:str):
    """ Download the data presented on the screen by using Qualtrics' built in download option (3 dots menu on the right of the table)

    Args:
        page (playwright.sync_api._generated.Page): page context
        download_location (str): Location of where to save the file
        org_short_name (str): Organizational name used in the file name
        filter_name (str): filter name used in file name
        filter_selection (str): the selected value from the filter (used in file name)
    """
    # hoover on the 3 dots
    page.get_by_label('Likert-scale statements - More options').hover()
    page.get_by_text('Export').click()
    page.locator('button[id="export-file-type-menu"]').click()
    page.get_by_text('CSV').click()

    # Start waiting for the download
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.locator('button[id="export-modal-export-button"]').click()
    download = download_info.value

    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as(download_location + "likert." + org_short_name + "." + filter_name + "." + filter_selection + ".csv")

    # close the download dialog
    page.locator('button[id="export-generate-close-btn"]').click()

    # don't use the section. See note in select_moe_statements()
    # reset table to default
    # page.get_by_text('Reset to Default').click()

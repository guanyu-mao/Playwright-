import os

def download_csv(page) -> None:
    """ Download daily consumption csv file from Azure

    Args:
        page (playwright.sync_api._generated.Page): page context
    """

    download_location = os.getenv('download_location', 'C:\azure_tables')

    with page.expect_download() as download_info:
        page.pause()
        page.get_by_role("button", name="Download").click()
        page.pause()
        page.get_by_role("radio", name="CSV").click()
        page.pause()
        page.get_by_role("button", name="Download data").click()
    download = download_info.value

    # Save the file to your desired location
    save_path = os.path.join(download_location, download.suggested_filename)
    download.save_as(save_path)
    print(f"Downloaded file saved to {save_path}")
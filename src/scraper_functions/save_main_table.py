import src.scraper_functions as scp
import os

def save_main_table(page,org:str,donwload_location:str=None):
    """ Download the main table with all filter set to `all`

    Args:
        page (playwright.sync_api._generated.Page): page context
        org (str): Organization for which to get the data
        donwload_location (str, optional): Where to save the data. Defaults to None.
    """
    if donwload_location is None:
        # load the download location
        donwload_location = os.getenv('download_location')

    scp.save_table_data(page,org_short_name=org, download_location=donwload_location,filter_name='all',filter_value_short='all')

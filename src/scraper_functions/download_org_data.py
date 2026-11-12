
import src.scraper_functions as scp
from dotenv import load_dotenv
import os

def download_org_data(page,org_short_name:str, download_location:str = None, datetime:str = None):
    """ Download all data for a selected org. Assume the site has been loaded and logged in.

    Args:
        page (playwright.sync_api._generated.Page): page context
        org_short_name (str): the org for which to download the data
        download_location (str, optional): the download location (optional). If not provided will get from `.env` file.
        datetime (str,optional): date and time used in the log file
    """
    ## where to save files on your computer
    if download_location is None:
         # load configuration file (user, password, dashboard_url, download location)
        load_dotenv(override=True)
        download_location=os.getenv('download_location')

    if download_location is None:
        raise NameError('you must provide download_location as an input or in the .env file')

    if datetime is None:
        # Other inputs
        # set date and time
        formatted_datetime = scp.datetime_timestamp()

    page = scp.select_org(page,org_short_name)

    # wait for 10s for everything to load
    # TODO #14
    page.wait_for_timeout(10000)

    # download main dataset
    scp.save_main_table(page,org = org_short_name)

    # download all data and store it to disk
    page = scp.download_filter(page,org_short_name=org_short_name, download_location=download_location)

    print('All data for ' + scp.get_org(org_short_name) +' downloaded')

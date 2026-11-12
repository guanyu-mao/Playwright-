import src.scraper_functions as scp
import pandas as pd
import io
import numpy as np
from typing import Optional

def save_table_data(page,org_short_name:str,download_location:str,filter_name:str,filter_value_short:str,fill_with_nulls:bool = False, filter_value_filename: Optional[str] = None):
    """Scrape(download) the first table showing on a page.

    Args:
        page (playwright.sync_api._generated.Page): page context
        org_short_name (str): organization name used when saving the file. Use short org name (e.g., for `Business Intelligence and Practice Division` use `bipd`)
        download_location (str): where on the disk to save the file (use full path names)
        filter_name (str): filter category selected (e.g. `region`). This is the short form identifier.
        filter_value_short (str): filter option from the filter category selected (e.g., `central_region`). This is the short form identifier
        fill_with_nulls (bool): if True the table will be filled with Nan instead of numbers
        filter_value_filename (Optional[str]):Optional file name used when using multiple filters (e.g., when downloading data grouped for anonymity)
    """
    # select the first table (its always the first table)
    table_html_full = scp.get_table(page)
    table_io = io.StringIO(table_html_full)
    pandas_table = pd.read_html(table_io)[0]

    column_names = ["question", "2024_response_count", "2024_response_mean", "2024_responsemean_moe", "2024_percent_favourable", "2024_percent_favourable_moe", "2022_response_count", "2022_response_mean", "2022_responsemean_moe", "2022_percent_favourable", "2022_percent_favourable_moe", "2021_response_count", "2021_response_mean", "2021_responsemean_moe", "2021_percent_favourable", "2021_percent_favourable_moe"]

    # change the column names to match Tarun's naming convention
    pandas_table.columns = column_names

    # replace `-` with nans
    # fixes #7
    if fill_with_nulls == False:
        # replaced to avoid setting pd.set_option('future.no_silent_downcasting', True)
        # see https://github.com/pandas-dev/pandas/issues/57734
        pandas_table = pandas_table.map(lambda x: np.nan if x=='-' else x)

    # fill the table with nulls if required
    # this is used when 'nodata' is found in the survey
    if fill_with_nulls == True:
       # extract the questions from the table (we don't want to replace those with NANs)
       questions_only = pandas_table['question']
       pandas_table_no_questions = pandas_table.drop(columns=['question'])

       # fill the rest of the data with NANs
       pandas_table_no_questions = pandas_table_no_questions.map(lambda x: np.nan)

       # add back the questions column and reorder
       pandas_table = pd.concat([questions_only, pandas_table_no_questions], axis=1)


    # add column with the org name, filter name, filter value
    pandas_table[['org', 'filter_name','filter_value']] = [org_short_name,filter_name,filter_value_short]

    # put our new columns first
    pandas_table = pandas_table[['org', 'filter_name','filter_value'] + pandas_table.columns[:-3].tolist()]

    if filter_value_filename is not None:
        filter_value_short = filter_value_filename

    # save the table to disk
    pandas_table.to_csv(download_location + "likert." + org_short_name + "." + filter_name + "." + filter_value_short + ".csv", index=False)

import src.scraper_functions as scp

def download_filter_option(page,filter_name:str,download_location:str,org_short_name:str):
    """ Loop through each filter option for a specified `filter_name` and save the table data by parsing through it rather then using the download option

    Args:
        page (playwright.sync_api._generated.Page): page context
        filter_name (str): short filter name (e.g., 'region'). For available options use the key in get_full_filter_text().
        download_location (str): Download location on the disk
        org_short_name (str): short organizational name. Used in the filename when storing the data.
    """

    # a dictionary of the form {'individual': {'sub0_2':'Central region'}}
    filter_options = scp.get_download_options(page,filter_name)

    # download the individual data for individual options
    options = filter_options['individual']
    if len(options)>0:
        for k,v in options.items():
            if v =='All':
                # skip downloading this one (we already did it initially)
                pass
            else:
                # save the data
                id = k
                scp.save_table(page,
                           type='data',
                           filter_name=filter_name,
                           download_id = id,
                           filter_description = scp.get_short_filter_description(v),
                           download_location = download_location,
                           org_short_name = org_short_name)
    # data grouped for anonymity
    options = filter_options['grouped']
    if len(options)>0:
        filter_value_short = ''
        for k,v in options.items():
            # combine all of the filter names into a single string used for savings
            # use the ; value as a separator
            # forward slash is already used in variable names
            filter_value_short = filter_value_short+scp.get_short_filter_description(v)+';'

            # get the id of when I need to click on
            # we will use the last element
            id = k
        # save the data
        scp.save_table(page,
                   type='data',
                   filter_name=filter_name,
                   download_id = id,
                   filter_description = filter_value_short,
                   download_location =  download_location,
                   org_short_name = org_short_name,
                   filter_value_filename='anonymized')

    options = filter_options['nodata']
    if len(options)>0:
        filter_value_short = ''
        for k,v in options.items():
            # combine all of the filter names into a single string used for savings
            # use the ; value as a separator
            # forward slash is already used in variable names
            filter_value_short = filter_value_short+scp.get_short_filter_description(v)+';'

        # save the data
        scp.save_table(page,
                   type='nodata',
                   filter_name=filter_name,
                   download_id = None,
                   filter_description = filter_value_short,
                   download_location =  download_location,
                   org_short_name = org_short_name,
                   filter_value_filename='nodata')

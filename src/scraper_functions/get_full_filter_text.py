import warnings
import os
import yaml

def get_full_filter_text(filter_short_text: str = "Default", direction: str = "short to full") -> str:
    """Convert a filter to its full filter text (e.g., `region` -> `Region filter`).
    Using direction = short will take full text filter (e.g., Region) and convert it to its short description
    Running the function without specifying a parameter will return all available filters shortcut codes and their corresponding name as they appear on Qualtrics's dashboard.

    Args:
        filter_short_text (str, optional): short filter name (e.g.,). Defaults to "Default".
        direction(str,optional): change the conversion direction (e.g., `region` -> `Region filter` to `Region filter` -> `region` )

    Returns:
        Union[dict,str]: return either the dictionary of all options or a single options as a string
    """
    #
    # TODO = check if there are repeating filters
    wd=os.getenv('working_directory')

    with open(wd+'data/'+'filters.yml', 'r') as config_file:
        all_filter_names = yaml.safe_load(config_file)

    # return the full text of the filter as shown on the page
    if filter_short_text == "Default":
        for k, v in all_filter_names.items():
            print(k+ ': "' +v+'"')
    elif filter_short_text == "DICTIONARY":
        return all_filter_names
    elif direction == "full to short":
        # create a new filter with no ' filter ' values at the end
        all_filter_names_no_filter = all_filter_names
        for key in all_filter_names_no_filter:
            all_filter_names_no_filter[key] = all_filter_names_no_filter[key].replace(' filter ', '')

        # invert the filter to go in the opposite direction
        all_filter_names_inverted = {value: key for key, value in all_filter_names_no_filter.items()}

        ret = all_filter_names_inverted.get(filter_short_text, 'undefined')

    else:
        ret = all_filter_names.get(filter_short_text, 'undefined')

    if ret == 'undefined':
        warnings.warn('Could not find requested filter ' + filter_short_text + ' in get_filter_full_text() function.')
    return ret

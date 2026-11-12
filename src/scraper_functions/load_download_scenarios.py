import yaml
from typing import Optional
import os
import src.scraper_functions as scp

def load_download_scenarios(file_name:str, wd:Optional[str] = None)->dict:
    """ Load a list of download scenarios defined in a yaml _name.

    Args:
        file_name (str): file name where the download scenarios are stored
        wd (Optional[str]): project working directory
    Returns:
        dict: a dictionary of scenarios ready for execution
    Dependencies:
        yaml
        typing
        os
        scp.scraper_functions
    """
    if scp.is_none(wd):
        wd=os.getenv('working_directory')

    if scp.is_none(wd):
        raise NameError('You must specify a working directory before loading orgs. Use the`.env` file or provide a location as an input to this function `load_orgs()`')

    # Load YAML file
    with open(wd+'data/scenarios/'+ file_name, 'r') as file:
        all_scenarios = yaml.safe_load(file)

    return all_scenarios

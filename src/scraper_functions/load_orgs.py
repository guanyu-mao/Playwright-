import os
from typing import Optional
import src.scraper_functions as scp
import yaml

def load_orgs(wd:Optional[str] = None) -> dict:
    """ Load a list of orgs for easy interactions

    Args:
        wd (Optional[str]): project working directory

    Returns:
        dict: a dictionary of options
    """
    if scp.is_none(wd):
        wd=os.getenv('working_directory')

    if scp.is_none(wd):
        raise NameError('You must specify a working directory before loading orgs. Use the`.env` file or provide a location as an input to this function `load_orgs()`')

    with open(wd+'data/'+'orgs.yml', 'r') as config_file:
        data = yaml.safe_load(config_file)

    return data

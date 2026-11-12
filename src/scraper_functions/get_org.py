import src.scraper_functions as scp
import warnings

def get_org(org_name:str, orgs:dict = None)-> str:
    """ Get the full name or short name of an org

    Args:
        org_name (str): Name of an org. Either full capitalized (e.g., Children, Community and Social Services) name or short name uncapitalized (e.g., bipd)
        orgs (Optional[dict]): option orgs dictionary containing the orgs list

    Returns:
        str: the full name of an org
    """
    if orgs is None:
        # load the orgs
        orgs = scp.load_orgs()

    # if the first letter of the org name is upper case then invert dictionary before looking for the org
    # this is how we distinguish between short and full org names
    if org_name[0].isupper():
        # invert the key value pair of the dictionary
        orgs_inverted = {value: key for key, value in orgs.items()}
        data = orgs_inverted.get(org_name,'undefined')
    else:
        data = orgs.get(org_name,'undefined')

    if data == "undefined":
        warnings.warn('Could not find the name for ' + org_name)

    return data

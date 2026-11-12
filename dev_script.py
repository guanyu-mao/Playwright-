import sys
import os
import importlib

# load custom functions needed for this script
os.chdir('E:/location/of/your/project/scp')
import src.scraper_functions as scp
importlib.reload(scp)
sys.modules

def m_reload():
    for k,v in sys.modules.items():
        if k.startswith('src'):
            importlib.reload(v)
# del sys.modules['src.scraper_functions.download_scenario']

# scenario download testing
m_reload()
org_name = "mccss"
page = scp.select_org(page,org_name)
scp.download_scenarios(page,"ardi_test.yml")

# when not using import list use this instead
sys.path.append(os.path.abspath('src'))
from scraper_functions import *
del sys.modules['scraper_functions']
from scraper_functions import *

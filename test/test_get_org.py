from src.scraper_functions import get_org
from dotenv import load_dotenv
load_dotenv(override=True)

def test_long_org():
    assert get_org("Children, Community and Social Services") == "mccss"

def test_short_org():
    assert get_org("mccss") == "Children, Community and Social Services"

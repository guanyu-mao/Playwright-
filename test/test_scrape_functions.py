from src.scraper_functions import get_full_filter_text
from dotenv import load_dotenv
load_dotenv(override=True)

def test_short_to_long():
    assert get_full_filter_text("region") == "Region filter "

def test_long_to_short():
    assert get_full_filter_text("Region","full to short") == "region"

from src.scraper.yelp.constants import CONSTANTS as YELP_CONSTANTS
from src.scraper.yelp.index import YelpScraper
from src.scraper.tripAdvisor.constants import CONSTANTS as TRIP_ADVISOR_CONSTANTS
from src.scraper.tripAdvisor.index import TripAdvisorScraper
import os
import sys

root = os.getcwd()
sys.path.append("{root}/src".format(root=root))

TAUrls = [
    # Place the url of any TripAdvisor search url
    # Example:
    'https://www.tripadvisor.com/Restaurants-g31377-Tempe_Arizona.html',
]

yelpUrls = [
    # Place the url of any Yelp search url
    # Example:
    "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Phoenix%2C%20AZ"
]

for url in TAUrls:
    TAScraper = TripAdvisorScraper(
        placesBreadth=2,
        paginationBreadth=2,
        queryUrl=TAUrls[0],
        saveToCSV=False,
        constants=TRIP_ADVISOR_CONSTANTS
    )
    print("Scraping TripAdvisor url: %s" % url)
    TAScraper.scrape()

for url in yelpUrls:
    YelpScraper = YelpScraper(
        placesBreadth=1,
        paginationBreadth=1,
        queryUrl=url,
        saveToCSV=False,
        constants=YELP_CONSTANTS
    )
    print("Scraping Yelp url: %s" % url)
    YelpScraper.scrape()

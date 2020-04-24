import requests
import sys
from bs4 import BeautifulSoup
from operator import itemgetter as destructure
from utils.decorators import classDecorator, exceptionHandler

from src.scraper.base.index import Scraper


@classDecorator(exceptionHandler)
class TripAdvisorScraper(Scraper):
    def __init__(self, queryUrl, constants, placesBreadth=1, paginationBreadth=1, saveToCSV=False):
        Scraper.__init__(self, queryUrl, constants,
                         placesBreadth, paginationBreadth, saveToCSV)
        self.type = "TripAdvisor"

    def constructPaginatedUrl(self, originalPlaceUrl, currentPage):
        start = currentPage * 10
        substring = "Reviews-"
        insertString = substring + "or{0}-".format(start)
        return insertString.join(originalPlaceUrl.split(substring))

    def getPlaceAddress(self, placeSoup):
        placeAddress = placeSoup.select(
            self.constants["PLACE_ADDRESS_CONTENT_SELECTOR"])[-1].text
        return placeAddress

    def getPlaceRating(self, placeSoup):
        ratingElement = placeSoup.select(
            self.constants["PLACE_RATING_ELEMENT_SELECTOR"])[0]
        rating = ratingElement.select(self.constants["PLACE_RATING_SELECTOR"])[
            0].get('alt').split(' of ')[0]
        return float(rating)

    def getReviewRating(self, review):
        rating = review.select(self.constants["REVIEW_RATING_SELECTOR"])[
            0].get("class")[-1]
        return float(rating.split(" ")[-1][-2:])/10

    def getPlaceName(self, place):
        return place.text.split(". ")[-1]

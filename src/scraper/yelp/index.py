from src.scraper.base.index import Scraper
from utils.decorators import classDecorator, exceptionHandler
from operator import itemgetter as destructure
import requests
from bs4 import BeautifulSoup


@classDecorator(exceptionHandler)
class YelpScraper(Scraper):
    def __init__(self, queryUrl, constants, placesBreadth=1, paginationBreadth=1, saveToCSV=False):
        Scraper.__init__(self, queryUrl, constants,
                         placesBreadth, paginationBreadth, saveToCSV)
        self.type = "Yelp"

    def constructPaginatedUrl(self, originalPlaceUrl, currentPage):
        start = (currentPage) * 20
        if "?" in originalPlaceUrl:
            insertString = "?start={0}&".format(start)
            pieces = originalPlaceUrl.split("?")
            paginatedUrl = insertString.join(pieces)
        else:
            insertString = "?start={0}".format(start)
            paginatedUrl = originalPlaceUrl + insertString
        return paginatedUrl

    def shouldSkipPlace(self, url):
        if ("/adredir" in url):
            return True

    def getTotalPages(self, placeSoup):
        return placeSoup.select(self.constants["LAST_PAGE_NUMBER_SELECTOR"])[0].text

    def getPlaceAddress(self, placeSoup):
        placeAddressElement = placeSoup.select(
            self.constants["PLACE_ADDRESS_SELECTOR"])[0]
        placeAddress = placeAddressElement.select(
            self.constants["PLACE_ADDRESS_CONTENT_SELECTOR"])[-1].text
        return placeAddress

    def getPlaceRating(self, placeSoup):
        rating = placeSoup.select(self.constants["PLACE_RATING_SELECTOR"])[
            0].get('aria-label')
        return float(rating.split(" ")[0])

    def getReviewRating(self, review):
        rating = review.select(self.constants["REVIEW_RATING_SELECTOR"])[
            0].get('aria-label')
        return float(rating.split(" ")[0])

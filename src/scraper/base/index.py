import requests
from urllib.parse import unquote
import pandas as pd
import sys
from bs4 import BeautifulSoup
import os
from utils.decorators import classDecorator, exceptionHandler
from operator import itemgetter as destructure
import csv


@classDecorator(exceptionHandler)
class Scraper:
    def __init__(self, queryUrl, constants, placesBreadth=1, paginationBreadth=1, saveToCSV=False):
        self.queryUrl = queryUrl
        self.constants = constants
        self.placesBreadth = placesBreadth
        self.paginationBreadth = paginationBreadth
        self.saveToCSV = saveToCSV
        self.type = "base"

    def scrape(self):
        HTML_PARSER, PLACE_SELECTOR, BASE_URL = destructure(
            'HTML_PARSER', 'PLACE_SELECTOR', 'BASE_URL')(self.constants)
        response = requests.get(self.queryUrl)
        placesSoup = BeautifulSoup(response.text, HTML_PARSER)
        if self.isRecaptchaPresent(placesSoup):
            print(
                "Recaptcha is present. Go to browser and complete recaptcha at any %s page." % self.type)
            return

        places = placesSoup.select(PLACE_SELECTOR)
        for placeIndex, place in enumerate(places):
            if (placeIndex < self.placesBreadth):
                placeName = self.getPlaceName(place)
                url = BASE_URL + place.get('href')
                if self.shouldSkipPlace(url):
                    continue
                else:
                    self.scrapePlace(url, placeName)
            else:
                break

    def isRecaptchaPresent(self, pageSoup):
        return len(pageSoup.findAll("script", {"src": "https://www.google.com/recaptcha/api.js"})) > 0

    def shouldSkipPlace(self, url):
        pass

    def constructPaginatedUrl(self, originalPlaceUrl, currentPage):
        pass

    def processReviewElement(self, review):
        pass

    def scrapePlace(self, originalPlaceUrl, placeName):
        HTML_PARSER, BASE_URL, REVIEWS_SELECTOR = destructure(
            'HTML_PARSER', 'BASE_URL', "REVIEWS_SELECTOR"
        )(self.constants)
        paginatedUrl = originalPlaceUrl

        reviewsData = []

        while True:
            placeHTML = requests.get(paginatedUrl).text
            placeSoup = BeautifulSoup(placeHTML, HTML_PARSER)
            if self.isRecaptchaPresent(placeSoup):
                print(
                    "Recaptcha is present. Go to browser and complete recaptcha at any %s page." % self.type)
                break
            totalPages = self.getTotalPages(placeSoup)
            currentPage = self.getCurrentPage(placeSoup)
            placeReviews = self.getReviewsElements(placeSoup)
            placeAddress = self.getPlaceAddress(placeSoup)
            placeRating = self.getPlaceRating(placeSoup)

            for reviewIndex, review in enumerate(placeReviews):
                reviewContent = self.getReviewContent(review)
                reviewRating = self.getReviewRating(review)
                reviewsData.append({
                    "source": self.type,
                    "placeName": placeName,
                    "placeAddress": placeAddress,
                    "placeRating": placeRating,
                    "reviewContent": reviewContent,
                    "reviewRating": reviewRating
                })
            pageMetadata = self.paginate(
                originalPlaceUrl, currentPage, totalPages)
            if pageMetadata["shouldPaginate"]:
                paginatedUrl = pageMetadata["nextPageUrl"]
                print("Paginating to: ", paginatedUrl)
            else:
                break

        # To save all data under data.csv
        self.addToCSV(data=reviewsData, keys=reviewsData[0].keys())

    def addToCSV(self, filename="data", data=[], keys=[]):
        filepath = './data/{0}.csv'.format(filename)
        with open(filepath, 'a', newline='\n') as file:
            if self.isCSVEmpty(filepath):
                writer = csv.writer(file)
                writer.writerow(keys)
            writer = csv.DictWriter(file, fieldnames=keys)
            for review in data:
                writer.writerow(review)
            file.close()

    def isCSVEmpty(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for index, _ in enumerate(reader):
                if index:
                    return False
            return True

    def paginate(self, originalPlaceUrl, currentPage, totalPages):
        shouldPaginate = currentPage != totalPages and currentPage < self.paginationBreadth
        return {
            "nextPageUrl": self.constructPaginatedUrl(originalPlaceUrl, currentPage),
            "shouldPaginate": shouldPaginate
        }

    def getCurrentPage(self, placeSoup):
        return int(placeSoup.select(self.constants["CURRENT_PAGE_NUMBER_SELECTOR"])[0].text)

    def getTotalPages(self, placeSoup):
        return int(placeSoup.select(self.constants["LAST_PAGE_NUMBER_SELECTOR"])[0].text)

    def getReviewsElements(self, placeSoup):
        return placeSoup.select(self.constants["REVIEWS_SELECTOR"])

    def getReviewContent(self, review):
        return review.select(self.constants["REVIEW_CONTENT_SELECTOR"])[0].text

    def getPlaceAddress(self, placeSoup):
        pass

    def getPlaceRating(self, placeSoup):
        pass

    def getReviewRating(self, review):
        pass

    def getPlaceName(self, place):
        return place.text

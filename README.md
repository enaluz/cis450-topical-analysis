# Topical Analysis + Yelp & TripAdvisor Scraper

## Table of Contents
[Purpose](#purpose)  
[Installation](#installation)  
[Usage](#usage)  
[Example Output](#example-output)  

## Purpose
A review scraper for Yelp & TripAdvisor and a simple topical analysis model using [LDA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html).

## Installation
1. Run `pip3 install -r requirements.txt`

## Usage
1. Scrape data by running `python3 index.py`. Paste custom links in `TAUrls` and `YelpUrls` from a location search page. 
<br/><br/>
Example for TripAdvisor: `https://www.tripadvisor.com/Restaurants-g31377-Tempe_Arizona.html`
<br/><br/>
Example for Yelp: `https://www.yelp.com/search?find_desc=Restaurants&find_loc=Phoenix%2C%20AZ`

## Example Output

```
Topic 1:
table, service, time, minutes, wait, came, place, server, asked, said

Topic 2:
flavor, really, got, ve, didn, eat, came, fries, make, stars

Topic 3:
ordered, eat, friend, salty, got, items, didn, came, really, customer

Topic 4:
taste, really, dishes, dirty, better, wait, time, definitely, long, flavor

Topic 5:
rude, service, bad, mean, pretty, little, ordered, expensive, price, ok
```
# To add a new cell, type ' '
# To add a new markdown cell, type '  [markdown]'
 
# import libraries
import numpy as np
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta 
def scrape():
    url = 'https://www.opentable.com/r/american-son-washington'
    response = requests.get(url)
    page_tree = BeautifulSoup(response.content, 'html.parser')

    divs = page_tree.main.div.find_all('div')
    
    # getting all reviews
    all_reviews = []
    for review in page_tree.select('p[id*="review-body-"]'):
        all_reviews.append(review.get_text())
    
    # getting dates
    # referenced this site: https://www.dataquest.io/blog/python-datetime-tutorial/https://www.dataquest.io/blog/python-datetime-tutorial/
    all_dates_span = page_tree.find_all("span", {"class": "oc-reviews-47b8de40"})
    all_dates = []
    for date in all_dates_span:
        curr = date.get_text()
        if 'on' in curr:
            curr = curr[9:]
            curr = datetime.strptime(curr, "%B %d, %Y")
        else:
            curr = curr[6:8]
            curr = int(curr.strip())
            now = datetime.now()
            # curr_str = '' + str(curr) + str(now.month) + str(now.year) + ''
            # curr_date = datetime.strptime(curr_str, "%d%m%Y")
            curr = now - timedelta(days=curr+1)
        all_dates.append(curr.date())
    
    review_df = pd.DataFrame(all_reviews, columns = ['review']) 
    review_df['date'] = all_dates
    
    # getting the all the ratings seperatly
    all_r = page_tree.find_all("div", {"class": "oc-reviews-0d90fee7"})
    overall = []
    food = []
    service = []
    ambiance = []
    for r in all_r:
        all_span_r = r.find_all('span', {'class': 'oc-reviews-e3e61235'})
        total = 0
        i = 0
        for sr in all_span_r:
            num = int(sr.get_text())
            if i == 0:
                overall.append(num)
            elif i == 1:
                food.append(num)
            elif i == 2:
                service.append(num)
            else:
                ambiance.append(num)
            i += 1
               
    # adding all review columns to the dataset
    review_df['overall_rating'] = overall
    review_df['food_rating'] = food
    review_df['service_rating'] = service
    review_df['ambiance_rating'] = ambiance
    
    review_df.to_csv('opentable_reviews.csv')
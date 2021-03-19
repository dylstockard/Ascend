
#import os
#import tarfile
import pandas as pd
#import json
#from nlp import Nlp
from reader import Reader
import report
from datetime import date
from datetime import timedelta

#PATH = os.path.dirname(os.path.abspath(__file__))
#
# Importing dataset from Yelp for scalable and automated solution.
#
# Unpacking tar file
'''
my_tar = tarfile.open('./yelp_dataset.tar')
my_tar.extractall(PATH) # specify which folder to extract to
my_tar.close()

# Loading datasets as iterators for space management.
reviews = pd.read_json("./yelp_academic_dataset_review.json", lines=True, chunksize=20)
businesses = pd.read_json("./yelp_academic_dataset_business.json", lines=True, chunksize=20)
'''



# Cleaning data
df = pd.read_csv('./opentable_reviews.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
df.columns = ('review', 'date', 'overall', 'food', 'service', 'ambiance')

today = date.today()
# Get current week
'''
curr_week = [today.strftime('%Y-%m-%d'),
        (today - timedelta(days=1)).strftime('%Y-%m-%d'),
        (today - timedelta(days=2)).strftime('%Y-%m-%d'),
        (today - timedelta(days=3)).strftime('%Y-%m-%d'),
        (today - timedelta(days=4)).strftime('%Y-%m-%d'),
        (today - timedelta(days=5)).strftime('%Y-%m-%d'),
        (today - timedelta(days=6)).strftime('%Y-%m-%d')]
is_curr_week = df['date'].isin(curr_week)
'''
# Get previous week
'''
prev_week = [(today - timedelta(days=7)).strftime('%Y-%m-%d'),
            (today - timedelta(days=8)).strftime('%Y-%m-%d'),
            (today - timedelta(days=9)).strftime('%Y-%m-%d'),
            (today - timedelta(days=10)).strftime('%Y-%m-%d'),
            (today - timedelta(days=11)).strftime('%Y-%m-%d'),
            (today - timedelta(days=12)).strftime('%Y-%m-%d'),
            (today - timedelta(days=13)).strftime('%Y-%m-%d')]
is_prev_week = df['date'].isin(prev_week)
'''
# Get current month dataframe as curr_month
is_curr_month = list(filter(lambda x: x.split('-')[1] == today.strftime('%m'), df['date']))
curr_month = df[df['date'].isin(is_curr_month)]
# Get previous month dataframe as prev_month
prev_month = (today.replace(day=1) - timedelta(days=1)).strftime('%m')
is_prev_month = list(filter(lambda x: x.split('-')[1] == prev_month, df['date']))
prev_month = df[df['date'].isin(is_prev_month)]

'''
# Cleaning for sample data
df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1, inplace=True)
df.drop([6, 10], inplace=True)
df.columns = ['Review']
df.reset_index(inplace=True)
df.drop(['index'], axis=1, inplace=True)
'''

# Creating NLP model and predicting reviews
#model = Nlp()
#sentiment = model.predict(df['review'])
#df['sentiment'] = sentiment

# Creating categorizer and printing/saving
#r = Reader(df)
#r.get_categories()
#r.analyze()

#report.create_report(df)
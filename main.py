
import os
#import tarfile
import pandas as pd
import json
#from nlp import Nlp
from reader import Reader
#import report

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
c = ('review', 'date', 'overall', 'food', 'service', 'ambiance')
df.columns = c

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
r = Reader(df)
r.get_categories()
r.analyze()

#report.create_report()

import os
import tarfile
import pandas as pd
import json
from nlp import Nlp
from reader import Reader

PATH = os.path.dirname(os.path.abspath(__file__))
#
# Importing dataset from Yelp for scalable and automated solution.
#
# Unpacking tar file
#my_tar = tarfile.open('./yelp_dataset.tar')
#my_tar.extractall(PATH) # specify which folder to extract to
#my_tar.close()

# Loading datasets as iterators for space management.
#reviews = pd.read_json("./yelp_academic_dataset_review.json", lines=True, chunksize=20)
#businesses = pd.read_json("./yelp_academic_dataset_business.json", lines=True, chunksize=20)

df = pd.read_excel('./SampleData.xlsx')
df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1, inplace=True)
df.drop([6, 10], inplace=True)
df.columns = ['Review']
df.reset_index(inplace=True)
df.drop(['index'], axis=1, inplace=True)

#model = Nlp()
#model.predict(test_file)

r = Reader(df)
r.print_categories()
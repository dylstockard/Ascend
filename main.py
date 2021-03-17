
import os
import tarfile
import pandas as pd
import json
from nlp import Nlp

PATH = os.path.dirname(os.path.abspath(__file__))
#
# Importing dataset from Yelp for scalable and automated solution.
#
# Unpacking tar file
#my_tar = tarfile.open('./yelp_dataset.tar')
#my_tar.extractall(PATH) # specify which folder to extract to
#my_tar.close()

# Loading reviews dataset
#reviews = pd.read_json("./yelp_academic_dataset_review.json", lines=True, chunksize=20)
#businesses = pd.read_json("./yelp_academic_dataset_business.json", lines=True, chunksize=20)

#matches = []
#in_dc = sample['state'] == 'DC'
#is_open = sample['is_open'] == 1
#is_postal = sample['postal_code'] == '20005'
#name = 'salter school'
#count = 0
#for sample in businesses:
    #index = sample.index[in_dc & is_open].tolist()
    #print(sample.loc[index, 'name'])
    #gotcha = sample.loc[sample.index[sample['state'].str.lower() == 'bc'], :]
    #print(gotcha['name'])
    #for row in sample:
        #print(row)
    #count += 1
    #if count == 5: break

test_file = './SampleData.xlsx'
model = Nlp()
model.predict(test_file)
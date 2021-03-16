
import os
import tarfile
import pandas as pd
import json

#PATH = os.path.dirname(os.path.abspath(__file__))
#
# Importing dataset from Yelp for scalable and automated solution.
#
#my_tar = tarfile.open('./yelp_dataset.tar')
#my_tar.extractall(PATH) # specify which folder to extract to
#my_tar.close()
#data = json.load(open("./yelp_academic_dataset_review.json", "r"))
#reviews = pd.DataFrame.from_dict(data, orient="index")


reviews = pd.read_excel('./SampleData.xlsx')
reviews.columns = ['review', 'service', 'date', 'analysis']
print(reviews)



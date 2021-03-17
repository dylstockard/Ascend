import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re


class Reader:

    # Takes a pandas dataframe reviews to analyze
    def __init__(self, reviews):
        self._map = pd.read_excel('./content_map.xlsx')
        self._categories = {key: {-1} for key in self._map.columns}
        self._categorize(reviews)
    
    def print_categories(self):
        print(self._categories)
    
    def _categorize(self, reviews):
        processed_reviews = []
        for review in reviews['Review']:
            processed_reviews.append(self._clean(review))
        p_reviews = pd.DataFrame(processed_reviews)
        p_reviews.columns = ['Review']
        for category in self._map:
            p_review_id = 0
            for p_review in p_reviews['Review']:
                line = p_review.split(' ')
                for word in line:
                    if self._map[category].str.contains(word).sum() > 0:
                        self._categories[category].add(p_review_id)
                p_review_id += 1
        for s in self._categories:
            self._categories[s].remove(-1)

    # Removes stop words, and lemmatizes given review
    def _clean(self, review):
        wl = WordNetLemmatizer()

        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = review.lower()
        review = review.split()
        review = [wl.lemmatize(word) for word in review if not word in all_stopwords]
        review = ' '.join(review)
        return review
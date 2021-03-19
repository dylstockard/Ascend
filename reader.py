import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')

WHITE = '#fafafa'
PINK = '#f7567c'
ORANGE = '#e59500'
BLUE = '#058ed9'
BLACK = '#777da7'

class Reader:

    # Takes a pandas dataframe reviews to analyze
    def __init__(self, reviews):
        temp = pd.read_excel('./content_map.xlsx')
        self._map = {key: temp[key].tolist() for key in temp.columns}
        # Remove NaN values
        for key in self._map.keys():
            self._map[key] = [x for x in self._map[key] if isinstance(x, str)]
        self._categories = {key: ({-1},{-1}) for key in self._map.keys()}
        self._categorize(reviews)
    
 
    def get_categories(self):
        return self._categories
    
 
    def get_categories_pos(self):
        pos = {key: self._categories[key][1] for key in self._categories.keys()}
        return pos


    def get_categories_neg(self):
        neg = {key: self._categories[key][0] for key in self._categories.keys()}
        return neg


    def analyze(self):
        self._count_reviews()
        self._percent_reviews()


    def _count_reviews(self):
        pos = self.get_categories_pos()
        neg = self.get_categories_neg()
        cat = pos.keys()
        pos_counts = [len(pos[l]) for l in pos]
        neg_counts = [len(neg[l]) for l in neg]

        fig, ax = plt.subplots(1,1)
        plt.bar(cat, pos_counts, label='positive', color=BLUE, bottom=neg_counts)
        plt.bar(cat, neg_counts, label='negative', color=ORANGE,)
        ax.set_facecolor(WHITE)
        ax.legend()

        plt.savefig('review_counts.png')


    def _percent_reviews(self):
        pos = self.get_categories_pos()
        neg = self.get_categories_neg()
        cat = pos.keys()
        # total review for each category
        totals = [(len(pos[c]) + len(neg[c])) for c in cat]
        pos_rev = [len(pos[l]) for l in pos]
        tot_pos = sum(pos_rev)
        tot_total = sum(totals)
        avg = tot_pos / tot_total
        percentages = {}
        i = 0
        for c in cat:
            positive_review_percent = int((pos_rev[i] / totals[i]) * 100)
            percentages[c] = [positive_review_percent]
            percentages[c].append(100 - positive_review_percent)
            i += 1
        percentages['overall'] = [int(avg * 100), (100 - int(avg * 100))]

        # graphing
        # make font larger and change style
        font = {'family' : 'Tahoma',
                'weight' : 'normal',
                'size' : 20}
        plt.rc('font', **font)

        labels = 'Positive', 'Negative'
        fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6]] = plt.subplots(3, figsize=(10, 20), ncols=2)
        sizes = percentages['food']
        ax1.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Food Reviews', fontsize=20, color=WHITE)
        ax1.tick_params(axis='x', colors='white')
        '''
        sizes = percentages['overall']
        ax2.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax2.set_title('Overall Reviews', fontsize=20, color=PINK)
        '''
        ax2.axis('off')

        sizes = percentages['brunch']
        ax3.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax3.set_title('Brunch Reviews', fontsize=20, color=WHITE)
                
        sizes = percentages['dinner']
        ax4.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax4.set_title('Dinner Reviews', fontsize=20, color=WHITE)

        sizes = percentages['ambiance']
        ax5.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax5.set_title('Ambiance Reviews', fontsize=20, color=WHITE)

        sizes = percentages['service']
        ax6.pie(sizes, labels=labels, shadow=True, autopct='%1.1f%%', startangle=90, labeldistance=None)
        ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax6.set_title('Service Reviews', fontsize=20, color=WHITE)


        ax1.legend(loc='upper right', bbox_to_anchor=(2.05,0.8))
        fig.patch.set_facecolor(BLACK)
        plt.savefig('all_piecharts.png')


    def _plot_piechart(self, category, percentages, ax):
        #labels = 'Positive', 'Negative'
        sizes = percentages[category]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, shadow=True, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(category + ' review percentages')
        plt.savefig(category + 'piechart.png')


    # reviews is a pandas dataframe
    def _categorize(self, reviews):
        p_reviews = reviews.copy()
        # Clean reviews for easier processing
        for i in range(len(reviews)):
            p_reviews.loc[i, 'review'] = self._clean(reviews.loc[i, 'review'])
        
        # Categorize reviews
        # for each category of the map:
        for c in self._map:
            # for each word in the map
            for w in self._map[c]:
                # for each review in the reviews
                for i in range(len(p_reviews)):
                    # Check if any matches from the reviews
                    if w in p_reviews.loc[i, 'review']:
                        # If greater or equal to 3, place in [1] (positive review)
                        rating = -1
                        if (c == 'brunch') | (c == 'dinner'):
                            rating = p_reviews.loc[i, 'food']
                        else:
                            rating = p_reviews.loc[i, c]
                        
                        # If there is a match, check if the rating is >= 3 stars
                        # If less than 3, place in [0] (negative review)
                        index = 0
                        if rating > 3:
                            index = 1
                        self._categories[c][index].add(i)
                        # Also add to brunch/dinner if category is food
                        if (c == 'brunch') | (c == 'dinner'):
                            self._categories['food'][index].add(i)
            self._categories[c][0].remove(-1)
            self._categories[c][1].remove(-1)

        '''
        Using sentiment analysis
        processed_reviews = reviews.copy()
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
        '''

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
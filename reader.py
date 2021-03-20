import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('ggplot')

TEAL = '#95D0F7'
TAN = '#EDDECD'
SILK = '#F2ECE5'
BLUE = '#6E9BB9'
GREY = '#858585'
BLACK = '#000000'
WHITE = '#FFFFFF'

PATH = './visuals/'

class Reader:

    # Takes a pandas dataframe reviews to analyze
    def __init__(self, reviews):
        self._reviews = reviews
        temp = pd.read_excel('./content_map.xlsx')
        self._map = {key: temp[key].tolist() for key in temp.columns}
        # Remove NaN values
        for key in self._map.keys():
            self._map[key] = [x for x in self._map[key] if isinstance(x, str)]
        self._categories = {key: ({-1},{-1}) for key in self._map.keys()}
        self._categorize()
    
 
    def get_categories(self):
        return self._categories
    
 
    def get_categories_pos(self):
        pos = {key: self._categories[key][1] for key in self._categories.keys()}
        return pos


    def get_categories_neg(self):
        neg = {key: self._categories[key][0] for key in self._categories.keys()}
        return neg


    def analyze(self):
        #self._count_reviews()
        maxes = self._percent_reviews()
        self._create_wordcloud(pos=True)
        self._create_wordcloud(pos=False)

        return maxes


    def get_helpful_reviews(self):
        '''
        Returns a tuple of dictionaries that contain 0=positive,
        1=negative reviews for each category
        '''
        g = self._helpful_reviews(self.get_categories_pos())
        n = self._helpful_reviews(self.get_categories_neg())
        all_helpful = (g, n)
        return all_helpful
    
    
    def _count_reviews(self):
        pos = self.get_categories_pos()
        neg = self.get_categories_neg()
        cat = pos.keys()
        pos_counts = [len(pos[l]) for l in pos]
        neg_counts = [len(neg[l]) for l in neg]

        fig, ax = plt.subplots(1,1)
        plt.bar(cat, pos_counts, label='positive', color=BLUE, bottom=neg_counts)
        plt.bar(cat, neg_counts, label='negative', color=PURPLE,)
        ax.set_facecolor(SILK)
        ax.legend()

        plt.savefig(PATH+'review_counts.png')


    def _percent_reviews(self):
        pos = self.get_categories_pos()
        neg = self.get_categories_neg()
        cat = pos.keys()
        # total review for each category
        totals = [(len(pos[c]) + len(neg[c])) for c in cat]
        pos_rev = [len(pos[l]) for l in pos]
        percentages = {}
        i = 0
        pos_max = ('default', -1)
        neg_max = ('default', -1)
        for c in cat:
            positive_review_percent = int((pos_rev[i] / totals[i]) * 100)
            percentages[c] = [positive_review_percent]
            percentages[c].append(100 - positive_review_percent)
            i += 1
            if positive_review_percent > pos_max[1]:
                pos_max = (c, positive_review_percent)
            elif (100 - positive_review_percent) > neg_max[1]:
                neg_max = (c, 100 - positive_review_percent)

        # graphing
        # make font larger and change style
        font = {'family' : 'Tahoma',
                'weight' : 'normal',
                'size' : 25}
        plt.rc('font', **font)

        labels = 'Positive', 'Negative'
        fig, [[ax1, ax2, ax3], [ax4, ax5, ax6]] = plt.subplots(2, figsize=(20, 10), ncols=3)
        title_color = BLACK
        title_size = 25
        sizes = percentages['food']
        ax1.pie(sizes, labels=labels, shadow=False, autopct='%1.0f%%', startangle=90, labeldistance=None, colors=[TEAL,BLUE])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Food Reviews', fontsize=title_size, color=title_color)
        
        ax2.axis('off')

        sizes = percentages['brunch']
        ax3.pie(sizes, labels=labels, shadow=False, autopct='%1.0f%%', startangle=90, labeldistance=None, colors=[TEAL,BLUE])
        ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax3.set_title('Brunch Reviews', fontsize=title_size, color=title_color)
                
        sizes = percentages['dinner']
        ax4.pie(sizes, labels=labels, shadow=False, autopct='%1.0f%%', startangle=90, labeldistance=None, colors=[TEAL,BLUE])
        ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax4.set_title('Dinner Reviews', fontsize=title_size, color=title_color)

        sizes = percentages['ambiance']
        ax5.pie(sizes, labels=labels, shadow=False, autopct='%1.0f%%', startangle=90, labeldistance=None, colors=[TEAL,BLUE])
        ax5.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax5.set_title('Ambiance Reviews', fontsize=title_size, color=title_color)

        sizes = percentages['service']
        ax6.pie(sizes, labels=labels, shadow=False, autopct='%1.0f%%', startangle=90, labeldistance=None, colors=[TEAL,BLUE])
        ax6.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax6.set_title('Service Reviews', fontsize=title_size, color=title_color)

        ax1.legend(loc='upper right', bbox_to_anchor=(2.05,1))
        fig.patch.set_facecolor(WHITE)
        plt.savefig(PATH+'all_piecharts.png', bbox_inches='tight', pad_inches=0)
        return (neg_max, pos_max)


    def _plot_piechart(self, category, percentages, ax):
        #labels = 'Positive', 'Negative'
        sizes = percentages[category]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, shadow=True, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(category + ' review percentages')
        plt.savefig(category + 'piechart.png')

    # Takes a dictionary of lists reviews to get review content
    # Takes boolean pos to determine if wordcloud is of positive or negative reviews
    # Takes a string cat that determins which category is displayed. Defaults to all.
    def _create_wordcloud(self, pos, cat='all'):
        data = {}
        stopwords = {'good',
                     'great',
                     'nice',
                     'bad',
                     'horrible',
                     'terrible',
                     'amazing',
                     'however',
                     'not',
                     'no',
                     'well',
                     'restaurant',
                     'definitely',
                     'go',
                     'really',
                     'week',
                     'would',
                     'overall',
                     'try',
                     'give',
                     'could',
                     'u',
                     'food',
                     'service',
                     'brunch'}
        label=''
        if pos:
            data = self.get_categories_pos()
            label = 'pos'
        else:
            data = self.get_categories_neg()
            label = 'neg'
        # Get all relevant rows
        all_rows = set()
        if cat == 'all':
            for val in data.values():
                all_rows = all_rows.union(val)
        else:
            try:
                all_rows = all_rows.union(data[cat])
            except KeyError:
                print('Invalid input parameter for \'cat\'')
                return None
        words = ''
        for row in all_rows:
            words += self._clean(self._reviews.loc[row, 'review'])
        wordcloud = WordCloud(stopwords=stopwords, width=1600, height=800, background_color=WHITE, max_words=100).generate(words)
        fig1, ax = plt.subplots(1,1)
        plt.figure(figsize=(2,1), dpi=400)
        plt.imshow(wordcloud, aspect='equal')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(PATH+'wordcloud_'+ cat + '_' + label + '.png', facecolor=None)


    def _helpful_reviews(self, reviews):
        '''
        creates a dictionary of reviews that has the categories
        as keys and reviews as the values
        '''
        review_dict= {}
        for c in reviews:
            review_dict[c] = []
            all_reviews = reviews[c]
            for r in all_reviews:
                if (len(self._reviews.loc[r, 'review']) > 200):
                    review_dict[c].append(self._reviews.loc[r, 'review'])
        return review_dict
    
    # reviews is a pandas dataframe
    def _categorize(self):
        p_reviews = self._reviews.copy()
        # Clean reviews for easier processing
        for i in range(len(p_reviews)):
            p_reviews.loc[i, 'review'] = self._clean(p_reviews.loc[i, 'review'])
        
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
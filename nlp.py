import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
import gensim
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import os

PATH = os.path.dirname(os.path.abspath(__file__))
url = "./GoogleNews-vectors-negative300.bin"
embeddings = gensim.models.KeyedVectors.load_word2vec_format(url, binary=True)

class Nlp:

    def __init__(self):
        self._model = self._train_model()

    def predict(self, file_path):
        df = pd.read_excel(file_path)
        df.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'], axis=1, inplace=True)
        df.drop([6, 10], inplace=True)
        df.columns = ['Review']
        df['Sentiment'] = [0] * len(df)
        df.reset_index(inplace=True)
        data = df.copy()
        #print(data.head())

        wl = WordNetLemmatizer()
        pre_text = []
        
        # Should make new method clean_data to remove redundancy
        for i in range(0, len(data)):
            all_stopwords = stopwords.words('english')
            all_stopwords.remove('not')
            review = re.sub('[^a-zA-Z]', ' ', data['Review'][i])
            review = review.lower()
            review = review.split()
            review = [wl.lemmatize(word) for word in review if not word in all_stopwords]
            review = ' '.join(review)
            pre_text.append(review)

        pre_data=pd.DataFrame(pre_text)
        print(pre_data.head())

        data.drop(['Review', 'index'],axis=1,inplace=True)
        data = pd.concat([pre_data,data],axis=1)
        print(data.head())
        data.columns = ['Review', 'Sentiment']

        docs_vectors = self._prepare_vectors(data)

        docs_vectors = docs_vectors.dropna()
        data['Sentiment'] = self._model.predict(docs_vectors)
        print(data.head())
        data.to_excel(PATH + '/output.xlsx')

    def _train_model(self):
        # Training dataset.
        url = 'Restaurant_Reviews.tsv'
        data = pd.read_csv(url, sep='\t', header = 0)

        # Columns renamed
        data.columns=['Review','Sentiment']

        # Text Preprocessing
        # Removing numbers, special characters, etc
        # Removal of stopwords
        # converting words to lowercase
        # Lemmatization
        wl = WordNetLemmatizer()

        pre_text = []
        for i in range(0, len(data)):
            all_stopwords = stopwords.words('english')
            all_stopwords.remove('not')
            review = re.sub('[^a-zA-Z]', ' ', data['Review'][i])
            review = review.lower()
            review = review.split()
            review = [wl.lemmatize(word) for word in review if not word in all_stopwords]
            review = ' '.join(review)
            pre_text.append(review)

        pre_data=pd.DataFrame(pre_text)
        pre_data.head()

        # %% [code]
        data.drop('Review',axis=1,inplace=True)
        data = pd.concat([pre_data,data],axis=1)
        data.columns =['Review','Sentiment']
        #print(data.head())

        docs_vectors = self._prepare_vectors(data)

        # %% [code]
        docs_vectors['Sentiment'] = data['Sentiment']
        docs_vectors = docs_vectors.dropna()

        # %% [code]
        # Head of Data
        #print(docs_vectors.head())

        # %% [code]
        # Train-Test split of Data
        from sklearn.model_selection import train_test_split

        x_train, x_test, y_train, y_test = train_test_split(docs_vectors.drop('Sentiment', axis=1),docs_vectors['Sentiment'], random_state=1)

        #print(x_test.head())

        # Support Vector Machine
        from sklearn import svm

        #Create a svm Classifier
        clf = svm.SVC(kernel='rbf') # Linear Kernel

        #Train the model using the training sets
        clf.fit(x_train, y_train)

        # Testing accuracy
        #y_pred=clf.predict(x_test)
        #print(y_pred)

        #confusion matrix
        #from sklearn.metrics import confusion_matrix
        #cm = confusion_matrix(y_pred, y_test)
        #print('Confusion Matrix: ', cm)

        #from sklearn.metrics import accuracy_score
        #accuracy = accuracy_score(y_pred, y_test)
        #print('Accuracy: ',accuracy)

        return clf

    def _prepare_vectors(self, data):
        # Preparing vectors for classification
        docs_vectors = pd.DataFrame()

        for doc in data['Review']:
            temp = pd.DataFrame()  # creating a temporary dataframe
            
            for word in doc.split(' '): # looping through each word of a single document and spliting through space
                
                try:
                    word_vec = embeddings[word] # if word is present in embeddings(provides weights associate with words(300)) then proceed
                    temp = temp.append(pd.Series(word_vec), ignore_index = True) # if word is present then append it to temporary dataframe
                except:
                    pass
            
            doc_vector = temp.mean() # take the average of each column(w0, w1, w2,........w300)
            #print(len(doc_vector))
            docs_vectors = docs_vectors.append(doc_vector, ignore_index = True) # append each document value to the final dataframe
        return docs_vectors
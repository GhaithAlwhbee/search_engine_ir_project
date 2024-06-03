from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

from Models.query import Query

app = FastAPI()


##########

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
import contractions
import string
import re



# Your preprocessing function
def my_preprocessor(doc):
        return doc  



##########

vectorizer = TfidfVectorizer(
                                preprocessor=my_preprocessor,
                                # lowercase=True,
                                # max_features=100000,
                                max_df=0.15,
                                min_df=5,
                                ngram_range = (1,1),
                                stop_words = "english"

                            )

def load_LifestyleDataset_vectorizer():
        with open('Data/LifestyleDataset/vectorizer.pkl', 'rb') as file:
                loaded_vectorizer = pickle.load(file)
                print("vectorizer loaded ..")
                return loaded_vectorizer
        
loaded_lifestyledataset_vectorizer = load_LifestyleDataset_vectorizer()


def load_ScienceDataset_vectorizer():
        with open('Data/ScienceDataset/vectorizer.pkl', 'rb') as file:
                loaded_vectorizer = pickle.load(file)
                print("vectorizer loaded ..")
                return loaded_vectorizer
        
loaded_sciencedataset_vectorizer = load_ScienceDataset_vectorizer()




@app.post("/indexing/vectories_docs")
def vectories_docs(data: dict):
        print("dataSetName: ",data['dataSetName'])
        vectors = vectorizer.fit_transform(data['cleaned_docs'])
        print("vectors.shape: ",vectors.shape)


        save_vectorizer(data['dataSetName'])
        save_matrix(data['dataSetName'],vectors)
        print("vectorizer & matrix are saved ..")

    


@app.post("/indexing/vectories_query")
def vectories_query(data: dict):
        if(data['datasetIndex'] == 0):

                np_array =  loaded_lifestyledataset_vectorizer.transform([data['query']]).toarray() 

        else:
                np_array =  loaded_sciencedataset_vectorizer.transform([data['query']]).toarray() 
                
        # print("query vector: ",np_array)
        # print("query vector to list: ",np_array)
        return np_array.tolist()



def save_vectorizer(dataSetName):
        Path = "Data/"+dataSetName+"/vectorizer.pkl"
        with open(Path, 'wb') as file:
            pickle.dump(vectorizer, file)



def save_matrix(dataSetName,matrix):
        Path = "Data/"+dataSetName+"/matrix_data.pkl"

        # Serialize and save to a binary file
        with open(Path, 'wb') as file:
                pickle.dump(matrix, file)



        
        

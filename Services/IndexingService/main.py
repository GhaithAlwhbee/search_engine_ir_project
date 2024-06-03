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
# def my_preprocessor(doc):
    
    
#     doc = re.sub(r'http\S+', '', doc)  # Remove URLs
#     doc = re.sub(r'<.*?>', '', doc)    # Remove HTML tags
#     doc = re.sub(r'\S+@\S+', '', doc)  # Remove email addresses
    
#     # Expanding the contractions
#     expanded_text = contractions.fix(doc)

#     # Converting the text to lowercase
#     lower_text = expanded_text.lower()

#     # Removing all special characters
#     no_shapes_text = lower_text.translate(str.maketrans('', '', string.punctuation))

    
#     return no_shapes_text

# def get_wordnet_pos(tag_parameter):

#         tag = tag_parameter[0].upper()
#         tag_dict = {"J": wordnet.ADJ,
#                     "N": wordnet.NOUN,
#                     "V": wordnet.VERB,
#                     "R": wordnet.ADV}
        
#         return tag_dict.get(tag, wordnet.NOUN)
    


# # Your tokenizer function
# def my_tokenizer(doc):
#     # Tokenizing the text
#     tokenized_text = word_tokenize(doc)

#     # POS tagging
#     pos_tags = pos_tag(tokenized_text)

#     # Removing the stop words and stemming the words
#     lemmatizer = WordNetLemmatizer()
#     stop_words = set(stopwords.words('english'))
#     processed_text = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word ,tag in pos_tags if word not in stop_words and not word.isdigit()]

#     return processed_text

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

    

# @app.post("/indexing/vectories_docs")
# def vectories_docs(cleaned_docs: list[str]):
        
#         vectors = vectorizer.fit_transform(cleaned_docs)

#         save_vectorizer()
#         save_matrix(vectors)
#         print("vectorizer & matrix are saved ..")

#         # print("vectors : ", vectors)
        # print("vectors 6 : ", vectors.getrow(6))

        # i=0
        # for vector in vectors:
        #     i+=1
        #     if i==9:
        #         print("vector 9 :", vector)

        # feature_names = vectorizer.get_feature_names_out()
        # df = pd.DataFrame(vectors.toarray(), columns=feature_names)
        # print(df)
        # return vectors

@app.post("/indexing/vectories_query")
def vectories_query(data: dict):
        if(data['datasetIndex'] == 0):

                np_array =  loaded_lifestyledataset_vectorizer.transform([data['query']]).toarray() 

        else:
                np_array =  loaded_sciencedataset_vectorizer.transform([data['query']]).toarray() 
                
        # print("query vector: ",np_array)
        # print("query vector to list: ",np_array)
        return np_array.tolist()

# @app.post("/indexing/vectories_query")
# def vectories_query(cleaned_query: Query,datasetIndex: int):
#         if(datasetIndex == 0):
#                 np_array =  loaded_lifestyledataset_vectorizer.transform([cleaned_query.query]).toarray() 
#         else:
#                 np_array =  loaded_sciencedataset_vectorizer.transform([cleaned_query.query]).toarray() 
                
#         # print("query vector: ",np_array)
#         # print("query vector to list: ",np_array)
#         return np_array.tolist()

def save_vectorizer(dataSetName):
        Path = "Data/"+dataSetName+"/vectorizer.pkl"
        with open(Path, 'wb') as file:
            pickle.dump(vectorizer, file)



def save_matrix(dataSetName,matrix):
        Path = "Data/"+dataSetName+"/matrix_data.pkl"

        # Serialize and save to a binary file
        with open(Path, 'wb') as file:
                pickle.dump(matrix, file)



        
        

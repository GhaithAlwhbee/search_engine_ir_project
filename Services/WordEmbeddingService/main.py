from gensim.models.doc2vec import Doc2Vec,\
    TaggedDocument
from nltk.tokenize import word_tokenize

from fastapi import FastAPI
app = FastAPI()
import pickle
import httpx


# define a list of documents.
data = ["This is the first document",
        "This is the second document",
        "This is the third document",
        "This is the fourth document"]
 

def load_LifestyleDataset_model():
        with open('Data/LifestyleDataset/model.pkl', 'rb') as file:
                loaded_vectorizer = pickle.load(file)
                print("vectorizer loaded ..")
                return loaded_vectorizer
        
loaded_lifestyledataset_model = load_LifestyleDataset_model()



@app.post("/embedding/vectories_embedding_docs")
def embedding_docs(data: dict):
    # preproces the documents, and create TaggedDocuments
    tagged_data = [TaggedDocument(words=word_tokenize(doc),
                                tags=[str(i)]) for i,
                doc in enumerate(data['cleaned_docs'])]
 
    # train the Doc2vec model
    model = Doc2Vec(vector_size=100,
                    min_count=2, epochs=50)
    model.build_vocab(tagged_data)
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.epochs)
    
    # get the document vectors
    embedded_vectors = [model.infer_vector(
        word_tokenize(doc)) for doc in data]
    
    
    #  print the document vectors
    # for i, doc in enumerate(data):
    #     print("Document", i+1, ":", doc)
    #     print("Vector:", document_vectors[i])

@app.post("/embedding/vectories_query")
def vectories_query(data: dict):
    #   if(data['datasetIndex'] == 0):
        np_array = loaded_lifestyledataset_model.infer_vector(word_tokenize(data['query']))
                # np_array =  loaded_sciencedataset_vectorizer.transform([data['query']]).toarray() 

        # else:
                # np_array =  loaded_lifestyledataset_vectorizer.transform([data['query']]).toarray() 
                # np_array =  loaded_sciencedataset_model.transform([data['query']]).toarray() 
                
        # print("query vector: ",np_array)
        # print("query vector to list: ",np_array)
        return np_array.tolist()

# dataSetName = "ScienceDataset"
dataSetName = "LifestyleDataset"


@app.post("/embedding/get_cleaned_docs_to_embedding")
async def get_cleaned_docs():
            # async with httpx.AsyncClient(timeout=None) as client:
            #     dataset = await client.get(f"http://localhost:8001/load_data_set/{dataSetName}")
            #     print("Dataset loaded ..")
            #     temp_dataset =[]
            #     i=0
            #     for doc in dataset.json():
            #         temp_dataset.append(doc)
            #         i += 1
            #         if (i>1000): break  
            #     return temp_dataset
            
            Path = "Data/"+dataSetName+"/cleanedDataSte.pkl"
            with open(Path, 'rb') as file:
                cleaned_dataset = pickle.load(file)
            
            temp_dataset =[]
            i=0
            for doc in cleaned_dataset.json():
                temp_dataset.append(doc)
                i += 1
                if (i>10000): break  

            print("cleaned Dataset loaded ..")
            index_payload = {
            "cleaned_docs": temp_dataset,
            "dataSetName": dataSetName
            }
            return temp_dataset

import re
import contractions
import string
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def get_wordnet_pos(tag_parameter):

        tag = tag_parameter[0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        
        return tag_dict.get(tag, wordnet.NOUN)
    
   
@app.post("/text_proccissing/clean_query")
def clean_query(data: dict):

    data['query'] = re.sub(r'http\S+', '', data['query'])  # Remove URLs
    data['query'] = re.sub(r'<.*?>', '', data['query'])    # Remove HTML tags
    data['query'] = re.sub(r'\S+@\S+', '', data['query'])  # Remove email addresses

    # Expanding the contractions
    expanded_text = contractions.fix(data['query'])

    # Converting the text to lowercase
    lower_text = expanded_text.lower()

    # Removing all special characters
    no_shapes_text = lower_text.translate(str.maketrans('', '', string.punctuation))


    # Tokenizing the text
    tokenized_text = word_tokenize(no_shapes_text)

    # POS tagging
    pos_tags = pos_tag(tokenized_text)

    # Removing the stop words and stemming the words
    processed_text = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word ,tag in pos_tags if word not in stop_words and not word.isdigit() ]#and word not in punctuation and word not in personal_pronouns
    processed_text = " ".join(processed_text)

    return processed_text
    # return processed_text


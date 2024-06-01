from fastapi import FastAPI
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from Models.query import Query
import contractions
import string
import re
from nltk import pos_tag
from nltk.corpus import wordnet


app = FastAPI()


# Creating a lemmatizer
lemmatizer = WordNetLemmatizer()
# Creating a stemmer
# ps = PorterStemmer()
# Defining the stop words
stop_words = set(stopwords.words('english'))
# Defining the punctuation
punctuation = set(string.punctuation)
# Defining the personal pronouns
personal_pronouns = set(['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs'])
# Processing the text
processed_docs = []

@app.post("/text_proccissing/clean_docs")
def clean_docs(docs: list[str]):
    for i,doc in enumerate(docs):

        # Expanding the contractions
        expanded_text = contractions.fix(doc)

        # Converting the text to lowercase
        lower_text = expanded_text.lower()

        # Removing all special characters
        no_shapes_text = lower_text.translate(str.maketrans('', '', string.punctuation))


        # Tokenizing the text
        tokenized_text = word_tokenize(no_shapes_text)

        # Removing the stop words and stemming the words
        processed_text = [lemmatizer.lemmatize(word) for word in tokenized_text if word not in stop_words and not word.isdigit() ]#and word not in punctuation and word not in personal_pronouns
        processed_text = " ".join(processed_text)

        processed_docs.append(processed_text)

        # Print progress
        if (i+1) % 10000 == 0:
            print(f'Processed {i+1} documents')

    return processed_docs



def get_wordnet_pos(tag_parameter):

        tag = tag_parameter[0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        
        return tag_dict.get(tag, wordnet.NOUN)
    


@app.post("/text_proccissing/clean_query")
def clean_query(queryObject: Query):

    queryObject.query = re.sub(r'http\S+', '', queryObject.query)  # Remove URLs
    queryObject.query = re.sub(r'<.*?>', '', queryObject.query)    # Remove HTML tags
    queryObject.query = re.sub(r'\S+@\S+', '', queryObject.query)  # Remove email addresses

    # Expanding the contractions
    expanded_text = contractions.fix(queryObject.query)

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

    return Query(query=processed_text).dict()
    # return processed_text


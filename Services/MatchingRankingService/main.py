from fastapi import FastAPI

from sklearn.metrics.pairwise import linear_kernel
import pickle
import httpx


app = FastAPI()


def load_LifestyleDataset_matrix():
        # To load the matrix back:
        with open('Data/LifestyleDataset/matrix_data.pkl', 'rb') as file:
                loaded_matrix = pickle.load(file)
                print("Lifestyle matrix loaded")
                return loaded_matrix

loaded_lifestyledataset_tfidf_matrix = load_LifestyleDataset_matrix()

def load_ScienceDataset_matrix():
        # To load the matrix back:
        with open('Data/ScienceDataset/matrix_data.pkl', 'rb') as file:
                loaded_matrix = pickle.load(file)
                print("Science matrix loaded")
                return loaded_matrix

loaded_sciencedataset_tfidf_matrix = load_ScienceDataset_matrix()

# def get_similarity_docs(self,query_vector,matrix):
#         i=0
#         for vector in matrix:
#             cosine = cosine_similarity(vector, query_vector)
#             if cosine > 0.9:
#                 print("vector ",i ,": ",vector)
#                 print ("cosine: ",cosine)
#             i+=1

    ############ 0.3 is best || 0.6 & 0.7  accept
# @app.post("/matching/get_similarity_docs_Ids")
# def get_similarity_docs(query_vector: list[list[float]],datasetIndex: int):
#         cosine_similarities = []
#         if(datasetIndex == 0):
#                 cosine_similarities = linear_kernel(query_vector, loaded_lifestyledataset_tfidf_matrix).flatten()
#         else:
#                 cosine_similarities = linear_kernel(query_vector, loaded_sciencedataset_tfidf_matrix).flatten()
#         # print("cosine_similarities : ",cosine_similarities)
#         # print(len(cosine_similarities.argsort()))# Top 10 
#         related_docs_indices = []
#         related_docs_indices = cosine_similarities.argsort()[:-11:-1] # Top 10 
#         # print("********************************************")
#         # print("query_vector : ",query_vector)
#         # print("related_docs_indices : ",related_docs_indices)
#         # print(cosine_similarities[related_docs_indices])
#         return related_docs_indices.tolist()

@app.post("/matching/get_similarity_docs_Ids")
def get_similarity_docs(data: dict):
        cosine_similarities = []
        if(data['datasetIndex'] == 0):
                print("get_similarity_docs_Ids from lifestyledataset")
                cosine_similarities = linear_kernel(data['query_vector'], loaded_lifestyledataset_tfidf_matrix).flatten()
        else:
                print("get_similarity_docs_Ids from sciencedataset")
                cosine_similarities = linear_kernel(data['query_vector'], loaded_sciencedataset_tfidf_matrix).flatten()
        # print("cosine_similarities : ",cosine_similarities)
        # print(len(cosine_similarities.argsort()))# Top 10 
        related_docs_indices = []
        related_docs_indices = cosine_similarities.argsort()[:-11:-1] # Top 10 
        # print("********************************************")
        # print("query_vector : ",query_vector)
        # print("related_docs_indices : ",related_docs_indices)
        # print(cosine_similarities[related_docs_indices])
        return related_docs_indices.tolist()





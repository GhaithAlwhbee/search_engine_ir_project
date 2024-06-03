from fastapi import FastAPI

from Models.query import Query
import httpx
import sqlite3


app = FastAPI()

conn = sqlite3.connect("Data/DataBase/ir_database.db")
cursor = conn.cursor()

@app.post("/read_query/from_user")
async def read_query(data: dict):
    # cleaned_query = p.clean_query(query)
    async with httpx.AsyncClient(timeout=None) as client:
        cleaned_query = await client.post(f"http://localhost:8002/text_proccissing/clean_query",json=data['query'])
        print("cleaned_query: ",cleaned_query.json())
        # indexing
        index_payload = {
            "query": cleaned_query.json()['query'],
            "datasetIndex": data['datasetIndex']
        }
        query_vector = await client.post(f"http://localhost:8003/indexing/vectories_query", json=index_payload)
        #Matching Ranking
        match_payload = {
            "query_vector": query_vector.json(),
            "datasetIndex": data['datasetIndex']
        }
        retrivedDocsIds = await client.post(f"http://localhost:8004/matching/get_similarity_docs_Ids", json=match_payload)
        
        print("retrivedDocsIds : ",retrivedDocsIds.json())
        retrivedDocs = get_docs_by_ids(retrivedDocsIds.json(),data['datasetIndex'])
        # return semilar docs
        # print("query_vector: ",query_vector.json())
        return retrivedDocs
      


# @app.post("/get_similarity_docs_Ids")
def get_docs_by_ids(item_ids: list,datasetIndex: int):
    placeholders = ', '.join('?' for _ in item_ids)
    if(datasetIndex == 0):
        cursor.execute(f"SELECT id, doc FROM lifestyleTable WHERE id IN ({placeholders})", item_ids)
    else:
        cursor.execute(f"SELECT id, doc FROM scienceTable WHERE id IN ({placeholders})", item_ids)
    docs = cursor.fetchall()
    # Create a dictionary with id as the key and doc as the value
    docs_dict = {id: doc for id, doc in docs}
    # Return docs in the order of item_ids
    ordered_docs = []
    for id in item_ids: 
        if id in docs_dict:
            ordered_docs.append({
                "id":id,
                "doc":docs_dict[id]
            })
    return ordered_docs


@app.post("/read_query/to_evaluate")
async def read_query_to_evaluate(data: dict):
    async with httpx.AsyncClient(timeout=None) as client:
        cleaned_query = await client.post(f"http://localhost:8002/text_proccissing/clean_query",json=data["query"])
        # indexing
        index_payload = {
            "query": cleaned_query.json()['query'],
            "datasetIndex": data['datasetIndex']
        }
        query_vector = await client.post(f"http://localhost:8003/indexing/vectories_query", json=index_payload,)
        #Matching Ranking
        match_payload = {
            "query_vector": query_vector.json(),
            "datasetIndex": data['datasetIndex']
        }
        retrivedDocsIds = await client.post(f"http://localhost:8004/matching/get_similarity_docs_Ids", json=match_payload)
        
        return retrivedDocsIds.json()

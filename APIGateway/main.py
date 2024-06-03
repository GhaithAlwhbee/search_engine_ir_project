from fastapi import FastAPI
import httpx

from Models.query import Query

app = FastAPI()

# Load DataSet Service API                  **********************

# dataSet name : LifestyleDataset
# dataSet name : ScienceDataset
@app.get("/load_data_set/{dataSetName}")
async def proxy_dataset(dataSetName: str):
    async with httpx.AsyncClient() as client:
        dataset_response = await client.get(f"http://localhost:8001/load_data_set/{dataSetName}")
    return dataset_response.json()
    

# Text proccissing Service API              **********************

@app.post("/text_proccissing/clean_query")
async def clean_query(queryObject: Query):
    async with httpx.AsyncClient() as client:
        cleaned_query_response = await client.post(f"http://localhost:8002/text_proccissing/clean_query",json=queryObject.dict())
        return cleaned_query_response.json()
    


# read query from user Service API          **********************

@app.post("/read_query/from_user")
async def read_query(query: Query,datasetIndex: int):
    async with httpx.AsyncClient(timeout=None) as client:
        print("datasetIndex: ",datasetIndex)
        payload = {
            "query": query.dict(),
            "datasetIndex": datasetIndex
        }
        matched_docs = await client.post(f"http://localhost:8005/read_query/from_user",json=payload)
        return matched_docs.json()
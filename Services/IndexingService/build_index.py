

import asyncio
import httpx
import time
import pickle


# dataSetName = "ScienceDataset"
dataSetName = "LifestyleDataset"



class BuildIndex:

    async def build_index(self):
        async with httpx.AsyncClient(timeout=None) as client:
            # dataset = await client.get(f"http://localhost:8001/load_data_set/{dataSetName}")
            # print("Dataset loaded ..")
            # cleaned_dataset = await client.post(f"http://localhost:8002/text_proccissing/clean_docs", json=dataset.json())

            Path = "Data/"+dataSetName+"/cleanedDataSte.pkl"
            with open(Path, 'rb') as file:
                cleaned_dataset = pickle.load(file)
            
            # temp_dataset =[]
            # i=0
            # for doc in cleaned_dataset.json():
            #     temp_dataset.append(doc)
            #     i += 1
            #     # if (i>10000): break  

            print("cleaned Dataset loaded ..")

            start_time = time.time()
            index_payload = {
            # "cleaned_docs": dataset.json(),
            "cleaned_docs": cleaned_dataset.json(),
            "dataSetName": dataSetName
            }
            await client.post(f"http://localhost:8003/indexing/vectories_docs", json=index_payload)
            print("Dataset vectoriesed ..")
            end_time = time.time()
            execution_time = (end_time - start_time)/60 
            print("indexing execution_time is : ",execution_time)
             
            # print(cleaned_dataset.json())
            print("tfidf_matrix build succssfully")





b = BuildIndex()
asyncio.run(b.build_index())
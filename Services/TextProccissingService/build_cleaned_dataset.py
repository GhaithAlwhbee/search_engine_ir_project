


import asyncio
import httpx
import time
import pickle



dataSetName = "ScienceDataset"
# dataSetName = "LifestyleDataset"




# def load_cleanedDataSet():
#         Path = "data/dataSetCleaned.pkl"
#         with open(Path, 'rb') as file:
#                 loaded_cleanedData = pickle.load(file)
#                 print(loaded_cleanedData)
        
# load_cleanedDataSet()

class BuildCleanedDataSet:
    async def build_cleaned_data_set(self):
        async with httpx.AsyncClient(timeout=None) as client:
            dataset = await client.get(f"http://localhost:8001/load_data_set/{dataSetName}")
            print("Dataset loaded ..")
            start_time = time.time()
            cleaned_dataset = await client.post(f"http://localhost:8002/text_proccissing/clean_docs", json=dataset.json())
            print("Dataset cleaned ..")

            Path = "Data/"+dataSetName+"/cleanedDataSte.pkl"
            with open(Path, 'wb') as file:
                pickle.dump(cleaned_dataset, file)
            
            
            end_time = time.time()
            execution_time = (end_time - start_time)/60 
            print("cleaned execution_time is : ",execution_time)
             
            # print(cleaned_dataset.json())
            print("cleaned DataSet build succssfully")



b = BuildCleanedDataSet()
asyncio.run(b.build_cleaned_data_set())
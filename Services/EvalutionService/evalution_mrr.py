import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import asyncio


# read qrels  
# P@K
# REL (k)
# AP@k
# MAP @K

import json
from typing import List
import httpx
from Models.qrel_query import QrelQuery




class MrrEvaluation:

    
    MRR = [] 
    listOfqrel = []

    def load_qrels(self,dataSetName):
        path = "Data/"+dataSetName+"/qas.forum.jsonl"
        with open(path) as qrel_json_file:
            for i,line in enumerate(qrel_json_file):
                json_obj = json.loads(line)
                qrel_query = QrelQuery(
                    qid= json_obj["qid"],
                    query= json_obj["query"],
                    score= json_obj["score"],
                    views= json_obj["views"],
                    answer_pids= json_obj["answer_pids"],
                )

                self.listOfqrel.append(qrel_query)
                if(i>10):break
            print("qrel length : ",len(self.listOfqrel))
            # for x in self.listOfqrel:
            #     print(x)



    async def evaluate(self,dataSetIndex):
        sum =0
        self.MRR.clear()
        for i,qrel in enumerate(self.listOfqrel):
            # print(qrel)
            self.MRR.append(await self.evaluate_query(qrel,dataSetIndex))
            if (i+1) % 100 == 0:
                print(f'Processed {i+1} qrel')
        for x in self.MRR:
            sum += x

        return sum/len(self.MRR)

    async def evaluate_query(self,queryObject: QrelQuery,dataSetIndex:int):
        retrived_docs = []
        async with httpx.AsyncClient() as client:
            payload = {
            "query": queryObject.dict(),
            "datasetIndex": dataSetIndex
            }
            retrived_docs = await client.post(f"http://localhost:8005/read_query/to_evaluate",json=payload)
        # print("retrived_docs: ",retrived_docs)
        # print("answer_pids: ",queryObject.answer_pids)
        for i,doc_id in enumerate(retrived_docs.json()):
            if(doc_id in queryObject.answer_pids):
                return 1/(i+1)
        return 0
        

    

    # def is_rel(self,doc_id,answer_pids):
    #     for pid in answer_pids:
    #         if pid == doc_id:
    #             return 1 
    #     return 0
     




# e = MrrEvaluation()
# e.load_qrels()
# print(e.evaluate())

dataSetName = "ScienceDataset"
dataSetIndex = 1

async def main():
    e = MrrEvaluation()
    e.load_qrels(dataSetName)
    print(await e.evaluate(dataSetIndex))



# Running the async main function
asyncio.run(main())



# e = MrrEvaluation()

# qrelQuery = QrelQuery(
#     qid = 23,
#     query="How do I get my cat to wear a tuxedo for several hours?",
#     score= 34,
#     views= 13479,
#     answer_pids=[1318, 1319, 1322, 1324, 1326, 1328, 1335]
# )
# print(e.evaluate_query(qrelQuery))


# e = MrrEvaluation()

# qrelQuery = QrelQuery(
#     qid = 0,
#     query="Why does my cat keep patting my face?",
#     score= 72,
#     views= 317697,
#     answer_pids=[116]
# )
# print(e.evaluate_query(qrelQuery))

# e = MrrEvaluation()

# qrelQuery = QrelQuery(
#     qid = 1,
#     query="How should I discipline my cat for bad behavior?",
#     score= 72,
#     views= 317697,
#     answer_pids=[32, 498, 1142, 3765, 4664, 6030, 7325, 7395, 9573]
# )
# print(e.evaluate_query(qrelQuery))


# e = MrrEvaluation()

# qrelQuery = QrelQuery(
#     qid = 4,
#     query="What is this street cat asking for, with continuous meowing?",
#     score= 55,
#     views= 19013,
#     answer_pids=[6106, 6107, 6116, 6119, 6121, 6135]
# )
# print(e.evaluate_query(qrelQuery))
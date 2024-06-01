
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
import time




class MapEvaluation:

    
    mapAtk  = 0  
    MRR  = 0 
    precision = 0
    recall = 0

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
                if(i>1000):break
            print("qrel length : ",len(self.listOfqrel))
            # for x in self.listOfqrel:
            #     print(x)



    async def evaluate(self,dataSetIndex):
        start_time = time.time()
        self.mapAtk_value  = 0  
        self.MRR_value  = 0 
        self.precision_value = 0
        self.recall_value = 0
        for i,qrel in enumerate(self.listOfqrel):
            # print(qrel)
            await self.evaluate_query(qrel,dataSetIndex)
            if (i+1) % 50 == 0:
                print(f'Processed {i+1} qrel')
                execution_time =  (time.time() - start_time)/60
                print("execution_time: ",execution_time)

        print("MAP : ",self.mapAtk_value/len(self.listOfqrel))
        print("MRR : ",self.MRR_value/len(self.listOfqrel))
        print("ReCall : ",self.recall_value/len(self.listOfqrel))
        

    async def evaluate_query(self,queryObject: QrelQuery,dataSetIndex: int):
        rows , cols = (2,10)
        pAtk = [[]]
        pAtk = [[0]*cols for _ in range(rows)]
        retrived_docs = []
        async with httpx.AsyncClient(timeout=None) as client:
            payload = {
            "query": queryObject.dict(),
            "datasetIndex": dataSetIndex
            }
            retrived_docs = await client.post(f"http://localhost:8005/read_query/to_evaluate",json=payload)
        # print("retrived_docs: ",retrived_docs)
        # print("answer_pids: ",queryObject.answer_pids)

        
        ## calculate MAP & Recall average
        numOfRelevantDocs = 0
        for i,doc_id in enumerate(retrived_docs.json()):
            if(doc_id in queryObject.answer_pids):
                # print("Matched : ",doc_id,queryObject.answer_pids)
                # print("Matched ",queryObject.qid)
                numOfRelevantDocs += 1
                pAtk[1][i] =  1
            else: pAtk[1][i] =  0
            pAtk[0][i] =  self.precision(i+1,pAtk)

        self.mapAtk_value += self.averagePAtK(pAtk)
        
        ## calculate MRR
        for i,doc_id in enumerate(retrived_docs.json()):
            if(doc_id in queryObject.answer_pids):
                self.MRR_value += 1/(i+1)
                break

        ## calculate ReCall
        self.recall_value += numOfRelevantDocs/len(queryObject.answer_pids)

        

    def averagePAtK(self,pAtk):
        sum =0
        numOfReleventDocs = 0
        for j,p in enumerate(pAtk[0]):
            if(pAtk[1][j] ==1):
                sum += pAtk[0][j]*pAtk[1][j]
                numOfReleventDocs += 1
        # print("averagePAtK : ",sum/10)
        return 0 if sum == 0 else sum/numOfReleventDocs


    def precision(self,i,pAtk):
        return self.NOR(pAtk)/i

    def NOR(self,pAtk):
        num =0
        for x in pAtk[1]:
            if x == 1:
                num+=1
        return num
    
    
    


#################   chose Dataset

dataSetName = "LifestyleDataset"
dataSetIndex = 0


# dataSetName = "ScienceDataset"
# dataSetIndex = 1

#################    ################# MapEvaluation  #################   ################# 


async def main():

    e = MapEvaluation()
    start_time = time.time()
    e.load_qrels(dataSetName)
    await e.evaluate(dataSetIndex)
    end_time = time.time()
    execution_time =  (end_time - start_time)/60
    print("map evaluation execution_time is : ",execution_time," m")




# Running the async main function
asyncio.run(main())

#################    ################# Average Precision @ K  #################   #################  


# qrelQuery = QrelQuery(
#     qid=23,
#     query="How do I get my cat to wear a tuxedo for several hours?",
#     score=34,
#     views=13479,
#     answer_pids=[1318, 1319, 1322, 1324, 1326, 1328, 1335]
# )

# async def main():
#     e = MapEvaluation()
#     e.load_qrels(dataSetName)
#     print(await e.evaluate_query(qrelQuery,dataSetIndex))



# # Running the async main function
# asyncio.run(main())


#################    ################# Recall  #################   #################   

# qrelQuery = QrelQuery(
#     qid=23,
#     query="How do I get my cat to wear a tuxedo for several hours?",
#     score=34,
#     views=13479,
#     answer_pids=[1318, 1319, 1322, 1324, 1326, 1328, 1335]
# )

# async def main():
#     e = MapEvaluation()
#     e.load_qrels(dataSetName)
#     print(await e.reCall(qrelQuery,dataSetIndex))


# # Running the async main function
# asyncio.run(main())

#################    #################          #################   #################   




# qrelQuery = QrelQuery(
#     qid = 1,
#     query="How should I discipline my cat for bad behavior?",
#     score= 72,
#     views= 317697,
#     answer_pids=[32, 498, 1142, 3765, 4664, 6030, 7325, 7395, 9573]
# )


# qrelQuery = QrelQuery(
#     qid = 4,
#     query="What is this street cat asking for, with continuous meowing?",
#     score= 55,
#     views= 19013,
#     answer_pids=[6106, 6107, 6116, 6119, 6121, 6135]
# )
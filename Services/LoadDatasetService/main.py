from fastapi import FastAPI


app = FastAPI()

#"Data/collection.tsv"

@app.get("/load_data_set/{dataSetName}")
async def loadData(dataSetName: str):
        dataset_List = []
        # self.dataset_List.clear()
        dataSetPath = "Data/"+dataSetName+"/collection.tsv"
        with open(dataSetPath) as file:
            i=0
            for line in file:
                l = line.split('\t')
                if(len(l)>1):
                    dataset_List.append(l[1])
                # i+=1
                # if i>10000:
                #     print ('num of docs:' ,i) 
                #     break
        return dataset_List
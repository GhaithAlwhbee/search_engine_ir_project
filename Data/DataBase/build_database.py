import sqlite3



# create empty database
connection = sqlite3.connect("ir_database.db")

# communicate with the database
cursor = connection.cursor()



def loadDataSet(dataSetName) :
    Path = "Data/"+dataSetName+"/collection.tsv"
    dataset_List = []
    with open(Path) as file:
        i=0
        for line in file:
            l = line.split('\t')
            if(len(l)>1):
                dataset_List.append((int(l[0]),l[1]))
            # i+=1
            # if i>2:
            #     print ('num of docs:' ,i) 
            #     break
    return dataset_List

scienceDataset = loadDataSet("ScienceDataset")
lifestyleDataset = loadDataSet("LifestyleDataset")


# create database table and populate it with release_list
cursor.execute("create table lifestyleTable (id integer, doc text)")
cursor.executemany("insert into lifestyleTable values (?,?)", lifestyleDataset)

cursor.execute("create table scienceTable (id integer, doc text)")
cursor.executemany("insert into scienceTable values (?,?)", scienceDataset)

# save changes immediatley
connection.commit()

# print all the rows from the gta table
# for row in cursor.execute("select * from lifestyleDS"):
#     print(row)

# print specific rows from the gta table
# print("******************************")
# cursor.execute("select * from gta where city=:c", {"c": "Liberty City"})
# gta_search = cursor.fetchall()
# print(gta_search)

# terminate the connection to "gta.db"
connection.close()





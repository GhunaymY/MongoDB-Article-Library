#Authors: Ghunaym Yahya and Maithili Jadhav
#Date: November 15, 2022
#Purpose: Takes a json file in the current directory and constructs a MongoDB collection.
#Resources: https://www.mongodb.com/languages/python
# https://www.freecodecamp.org/news/python-read-json-file-how-to-load-json-from-a-file-and-parse-dumps/
# https://hevodata.com/learn/json-to-mongodb-python/
from pymongo import MongoClient, TEXT
import os

port = input("port number: ")
my_file = input("file: ")
#We must ensure that the port number entered by the user is valid. We will use a try and except to check whether or not the port number is valid.
try: 
    myclient = MongoClient("mongodb://localhost:{}/".format(port))
except:
    print("Invalid port number.") #If there was an error in the try block we will exit the program and give an Invalid port number error to the user. 
    exit()

lists = myclient.list_database_names()
if '291db' in lists:
    print("db exists already")
    db = myclient["291db"]
else:
    print("creating new db")
    db = myclient["291db"]

def load(my_file):
    global myclient, db
    collection = db["dblp"]
    if collection.drop(): # sees if there is an existing collection
        db.drop_collection("dblp")
        collection = db["dblp"]
        print("Existing dplp dropped...new one created!")
    #The following block of code will read our json file into python.
    os.system("mongoimport --db 291db --collection dblp --file " + my_file + " --port " + str(port) + " --batchSize 1000 --numInsertionWorkers 10")
    for col in db.list_collection_names(): #changing year to string for phase 2
        db[col].update_many({'year': {'$exists': True, '$type': 'int'}}, [{'$set': {'year': { '$toString': '$year'}}}])
    collection.create_index([("title",TEXT),("authors",TEXT),("abstract",TEXT),("venue",TEXT),("year",TEXT),("references",TEXT)],default_language = 'none')  #creating index for optimizing searches

def main():
    load(my_file)

if __name__ == '__main__':
    main()







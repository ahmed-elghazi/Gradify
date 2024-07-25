import unittest
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def hitTheDB(name: str):
    uri = "mongodb+srv://ahmed:Bqxgz4Mc3eLtUlGj@courses-profs.locvj1l.mongodb.net/?retryWrites=true&w=majority&appName=Courses-Profs"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['university_db']
    collection = db['instructors']
    query = {'name': name}
    filtered_documents = collection.find(query)
    document = filtered_documents[0]
    total = document['ratings']['4.0'] + document['ratings']['Pass'] + document['ratings']['Fail'] + document['ratings']['Withdraw']
    list = {
        "4.0": round((document['ratings']['4.0'] / total) * 100),
        "Pass": round((document['ratings']['Pass'] / total) * 100),
        "Fail": round((document['ratings']['Fail'] / total) * 100),
        "Withdraw": round((document['ratings']['Withdraw'] / total) * 100)
    }
    print(list)
    return list

if(__name__ == "__main__"):
    hitTheDB("Jason Smith")
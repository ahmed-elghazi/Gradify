import unittest
from pymongo import MongoClient  # Import for MongoDB connection
from pymongo.server_api import ServerApi  # Import for specifying server API version

def hitTheDB(name: str):
    uri = "mongodb+srv://github:XYDhRYbc0KGMb6BN@courses-profs.locvj1l.mongodb.net/?retryWrites=true&w=majority&appName=Courses-Profs"  # MongoDB connection URI redacted
    client = MongoClient(uri, server_api=ServerApi('1'))  # Connect to MongoDB server
    db = client['university_db']  # Access the database
    collection = db['instructors']  # Access the instructors collection
    query = {'name': name}  # Query to find the instructor by name
    filtered_documents = collection.find(query)  # Execute the query
    try:
        document = filtered_documents[0]  # Attempt to get the first matching document
    except IndexError:
        print("No document found.")  # Handle case where no document is found
        return None
    total = document['ratings']['4.0'] + document['ratings']['Pass'] + document['ratings']['Fail'] + document['ratings']['Withdraw']  # Calculate total ratings
    list = {
        "4.0": round((document['ratings']['4.0'] / total) * 100),  # Calculate percentage of 4.0 ratings
        "Pass": round((document['ratings']['Pass'] / total) * 100),  # Calculate percentage of Pass ratings
        "Fail": round((document['ratings']['Fail'] / total) * 100),  # Calculate percentage of Fail ratings
        "Withdraw": round((document['ratings']['Withdraw'] / total) * 100)  # Calculate percentage of Withdraw ratings
    }
    return list  # Return the list of grade percentages

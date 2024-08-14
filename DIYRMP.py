import requests  # For sending HTTP requests
import re  # Regex module for string matching
import json  # For handling JSON data
import base64  # For encoding data
import os  # For interacting with the operating system
import time  # For performance tracking
from bs4 import BeautifulSoup  # For parsing HTML

# Paths to JSON files and headers (you can customize these paths as per your project structure)
current_path = os.path.dirname(__file__)  # Get the directory of the current file
professor_query_file = os.path.join(current_path, "json/professorquery.json")  # Path to professor query JSON file
header_file = os.path.join(current_path, "json/header.json")  # Path to header JSON file

# Load JSON files
with open(professor_query_file, 'r') as f:
    professor_query = json.load(f)  # Load professor query data from JSON file

with open(header_file, 'r') as f:
    headers = json.load(f)  # Load HTTP headers from JSON file


def get_schools_by_name(school_name: str):
    school_name.replace(' ', '+')  # Replace spaces with '+' for URL encoding
    url = "https://www.ratemyprofessors.com/search/schools?q=%s" % school_name  # Build URL to search for schools
    page = requests.get(url)  # Send HTTP GET request
    data = re.findall(r'"legacyId":(\d+)', page.text)  # Extract legacy IDs from the response using regex

    if data:
        try:
            return [int(data[0])]  # Return only the first school found (as a list)
        except ValueError:
            pass

    return []  # Return empty list if no schools found


def get_professors_by_school_and_name(college: int, professor_name: str):
    url = 'https://www.ratemyprofessors.com/search/professors/%s?q=%s' % (college, professor_name)  # Build URL to search for professors
    page = requests.get(url)  # Send HTTP GET request
    data = re.findall(r'"legacyId":(\d+)', page.text)  # Extract professor IDs from the response using regex
    professor_list = []

    if data:
        try:
            professor_list = [int(prof_id) for prof_id in data]  # Convert extracted IDs to integers
        except ValueError:
            pass

    return professor_list  # Return list of professor IDs


def get_professor_ratings(professor_id: int):
    headers["Referer"] = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor_id  # Update referer header
    professor_query["variables"]["id"] = base64.b64encode(("Teacher-%s" % professor_id).encode('ascii')).decode('ascii')  # Encode professor ID for the query
    data = requests.post(url="https://www.ratemyprofessors.com/graphql", json=professor_query, headers=headers)  # Send POST request with professor query

    if data is None or json.loads(data.text)["data"]["node"] is None:  # Check if the response is valid
        raise ValueError("Professor not found with that id or bad request.")

    professor_data = json.loads(data.text)["data"]["node"]  # Extract professor data from the response
    results = [
        professor_data["firstName"],
        professor_data["lastName"],
        professor_data["avgRating"],
        professor_data["avgDifficulty"],
        "N/A" if professor_data["wouldTakeAgainPercent"] == -1 else professor_data["wouldTakeAgainPercent"]  # Handle edge case for 'would take again' percentage
    ]

    return results  # Return the professor's ratings and other details


def find_correct_professor(college: int, professor_name: str):
    professors = get_professors_by_school_and_name(college, professor_name)  # Get list of professors by school and name
    for professor_id in professors:
        details = get_professor_ratings(professor_id)  # Get the ratings for each professor ID
        full_name = f"{details[0]} {details[1]}"  # Combine first and last names
        full_name2 = f"{details[1]} {details[0]}"
        if full_name.lower() == professor_name.lower():  # Match the full name with the searched name
            return details  # Return the correct professor's details
    return None  # Return None if no matching professor is found


def testAPI(name):
    return find_correct_professor(1273, name)  # Test function to find a professor by name


def main():
    result = testAPI("Alexandre Pinheiro")  # Example test call
    if result:
        print(result)  # Print the result if found
    else:
        print("Professor not found.")  # Print an error message if not found

if __name__ == "__main__":
    main()  # Execute the main function when the script is run directly

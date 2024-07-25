import requests
import re
import json
import base64
import os
import time
import datetime
from bs4 import BeautifulSoup
from functools import total_ordering

# Assuming you have already defined the Professor and Rating classes as discussed earlier

# Paths to JSON files and headers (you can customize these paths as per your project structure)
current_path = os.path.dirname(__file__)
professor_query_file = os.path.join(current_path, "json/professorquery.json")
header_file = os.path.join(current_path, "json/header.json")

# Load JSON files
with open(professor_query_file, 'r') as f:
    professor_query = json.load(f)

with open(header_file, 'r') as f:
    headers = json.load(f)


def get_schools_by_name(school_name: str):
    school_name.replace(' ', '+')
    url = "https://www.ratemyprofessors.com/search/schools?q=%s" % school_name
    page = requests.get(url)
    data = re.findall(r'"legacyId":(\d+)', page.text)

    if data:
        try:
            return [int(data[0])]  # Return only the first school found
        except ValueError:
            pass

    return []  # Return empty list if no schools found


def get_professors_by_school_and_name(college: int, professor_name: str):
    url = 'https://www.ratemyprofessors.com/search/professors/%s?q=%s' % (college, professor_name)
    page = requests.get(url)
    data = re.findall(r'"legacyId":(\d+)', page.text)
    professor_list = []

    if data:
        try:
            professor_list.append(int(data[0]))  # Append only the first professor found
        except ValueError:
            pass

    return professor_list


def get_professor_ratings(professor_id: int):
    headers["Referer"] = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor_id
    professor_query["variables"]["id"] = base64.b64encode(("Teacher-%s" % professor_id).encode('ascii')).decode('ascii')
    data = requests.post(url="https://www.ratemyprofessors.com/graphql", json=professor_query, headers=headers)

    if data is None or json.loads(data.text)["data"]["node"] is None:
        raise ValueError("Professor not found with that id or bad request.")

    results = []

    professor_data = json.loads(data.text)["data"]["node"]
    # avg_rating = professor_data["avgRating"]
    # avg_difficulty = professor_data["avgDifficulty"]
    # would_take_again_percent = professor_data["wouldTakeAgainPercent"]
    results.append(professor_data["firstName"])
    results.append(professor_data["lastName"])
    results.append(professor_data["avgRating"])
    results.append(professor_data["avgDifficulty"])
    if professor_data["wouldTakeAgainPercent"] == -1:
        results.append("N/A")
    else:
        results.append(professor_data["wouldTakeAgainPercent"])

    #return Rating(rating=avg_rating, difficulty=avg_difficulty, take_again=would_take_again_percent)
    #return f"Rating: {avg_rating}, Difficulty: {avg_difficulty}, Take Again %: {would_take_again_percent}"
    #return f"Name: {professor_data["firstName"]} {professor_data["lastName"]}, Rating: {avg_rating}, Difficulty: {avg_difficulty}, Take Again %: {would_take_again_percent:.2f}"
    return results

def testAPI(name):
    prof = get_professors_by_school_and_name(1273, name)
    return get_professor_ratings(prof[0])



def main():
    # start_time = time.time()
    # school = get_schools_by_name("The University of Texas at Dallas")
    # print(school)
    # print((time.time() - start_time))

    # start_time = time.time()
    # professors = get_professors_by_school_and_name(1273, "Nhut Nguyen")
    # print(professors)
    # print(time.time() - start_time)

    # # Example usage to get ratings for the first professor found
    # if professors:
    #     professor_id = professors[0]
    #     rating = get_professor_ratings(professor_id)
    #     print(rating)
    # else:
    #     print("No professors found.")
    # print(time.time() - start_time)
    testAPI("Scott Dollinger")

if __name__ == "__main__":
    main()

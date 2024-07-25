import requests
import re
import json
import base64
import os
import time
from bs4 import BeautifulSoup

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
            professor_list = [int(prof_id) for prof_id in data]
        except ValueError:
            pass

    return professor_list


def get_professor_ratings(professor_id: int):
    headers["Referer"] = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor_id
    professor_query["variables"]["id"] = base64.b64encode(("Teacher-%s" % professor_id).encode('ascii')).decode('ascii')
    data = requests.post(url="https://www.ratemyprofessors.com/graphql", json=professor_query, headers=headers)

    if data is None or json.loads(data.text)["data"]["node"] is None:
        raise ValueError("Professor not found with that id or bad request.")

    professor_data = json.loads(data.text)["data"]["node"]
    results = [
        professor_data["firstName"],
        professor_data["lastName"],
        professor_data["avgRating"],
        professor_data["avgDifficulty"],
        "N/A" if professor_data["wouldTakeAgainPercent"] == -1 else professor_data["wouldTakeAgainPercent"]
    ]

    return results


def find_correct_professor(college: int, professor_name: str):
    professors = get_professors_by_school_and_name(college, professor_name)
    for professor_id in professors:
        details = get_professor_ratings(professor_id)
        full_name = f"{details[0]} {details[1]}"
        full_name2 = f"{details[1]} {details[0]}"
        if full_name.lower() == professor_name.lower():
            return details
    return None


def testAPI(name):
    return find_correct_professor(1273, name)


def main():
    result = testAPI("Alexandre Pinheiro")
    if result:
        print(result)
    else:
        print("Professor not found.")


if __name__ == "__main__":
    main()

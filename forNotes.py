import requests
from bs4 import BeautifulSoup

# Define the base URL for Rate My Professors
BASE_URL = "https://www.ratemyprofessors.com"

# Define a function to search for a professor by first and last name at a specific school
def search_professor(first_name, last_name, school_id):
    # Construct the search URL with the provided school ID and professor's name
    search_url = f"{BASE_URL}/search/professors/{school_id}?q={first_name}%20{last_name}"
    
    # Make a GET request to search for the professor
    response = requests.get(search_url)
    
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    print(soup)
    
    # Find the first professor in the search results
    professor_div = soup.find('div', class_='CardName__StyledCardName-sc-1gyrgim-0 fVGTbR')
    
    if professor_div:
        # Extract the professor's ID from the link
        professor_link = professor_div.find('a')['href']
        professor_id = professor_link.split('/')[-1]
        
        # Return the professor ID
        return professor_id
    else:
        # If no professor is found, return None
        return None

# Define a function to get the detailed ratings of a professor
def get_professor_ratings(professor_id):
    # Construct the URL to get ratings for the professor
    ratings_url = f"{BASE_URL}/ShowRatings.jsp?tid={professor_id}"
    
    # Make a GET request to get the professor's ratings
    response = requests.get(ratings_url)
    
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Extract the ratings information
    quality = soup.find('div', class_='RatingValue__Numerator-qw8sqy-2 gxuTRq').text.strip()
    difficulty = soup.find_all('div', class_='RatingValue__Numerator-qw8sqy-2 gxuTRq')[1].text.strip()
    take_again = soup.find('div', class_='FeedbackItem__FeedbackNumber-uof32n-1 kkESWs').text.strip()
    
    # Return the ratings as a dictionary
    return {
        'quality': quality,
        'difficulty': difficulty,
        'take_again': take_again
    }

# Main function to execute the program
def main():
    # Define the school ID (1273 in this case)
    school_id = 1273
    
    # Prompt the user to input the professor's first and last name
    #first_name = input("Enter the professor's first name: ")
    #last_name = input("Enter the professor's last name: ")

    first_name = "Nhut"
    last_name = "Nguyen"
    
    # Search for the professor
    professor_id = search_professor(first_name, last_name, school_id)
    
    # Check if the professor was found
    if professor_id:
        # Get the professor's ratings
        ratings = get_professor_ratings(professor_id)
        
        # Check if ratings are found
        if ratings:
            # Print the professor's ratings
            print(f"Quality: {ratings.get('quality', 'N/A')}")
            print(f"Difficulty: {ratings.get('difficulty', 'N/A')}")
            print(f"Take Again Percentage: {ratings.get('take_again', 'N/A')}")
        else:
            # If no ratings are found, inform the user
            print("No ratings found for this professor.")
    else:
        # If no professor is found, inform the user
        print("Professor not found.")

# Execute the main function
if __name__ == "__main__":
    main()

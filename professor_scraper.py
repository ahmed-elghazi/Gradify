import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")

BASE_URL = "https://www.ratemyprofessors.com"

def scrape_professor_info(school_id, first_name, last_name):
    start_time = time.time()
    
    # Set up the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    #driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    search_url = f"{BASE_URL}/search/professors/{school_id}?q={first_name}%20{last_name}"
    driver.get(search_url)

    # Wait for the specific element to be loaded COMMENTED FOR EFFECIENCY SAKE
    # try:
    #     WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "TeacherCard__InfoRatingWrapper-syjs0d-3"))
    #     )
    # except:
    #     driver.quit()
    #     return {"error": "Timeout waiting for page to load"}

    # Get the page source after the element is loaded
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    #professors = {'Omar Hamdy', 'Sridhar Alagar', 'Emily Fox', 'Serdar Erbatur', 'Greg Ozbirn', 'Ziaullah Khan'}
    
    professor = soup.find('div', class_='TeacherCard__InfoRatingWrapper-syjs0d-3')
    if professor:
        quality = professor.find('div', class_='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2').text
        name = professor.find('div', class_='CardName__StyledCardName-sc-1gyrgim-0').text
        take_again = professor.find('div', class_='CardFeedback__CardFeedbackNumber-lq6nix-2').text
        difficulty = professor.find_all('div', class_='CardFeedback__CardFeedbackNumber-lq6nix-2')[1].text

        end_time = time.time()
        execution_time = end_time - start_time
        print("SUCESSFUL SCRAPE")

        return {
            'name': name,
            'quality': quality,
            'take_again': take_again,
            'difficulty': difficulty,
            'execution_time': execution_time
        }
    else:
        return {"error": "No professor information found"}
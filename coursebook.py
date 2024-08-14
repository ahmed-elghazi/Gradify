import time
from selenium import webdriver  # Import for web scraping
from selenium.webdriver.common.by import By  # For locating elements by XPath
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # Utility for managing the ChromeDriver
from selenium.webdriver.chrome.options import Options  # For configuring ChromeDriver options
from selenium.webdriver.support.ui import WebDriverWait  # For implementing waits
from selenium.webdriver.support import expected_conditions as EC  # For setting expected conditions for waits
from bs4 import BeautifulSoup  # For parsing HTML
import re  # Regex module for string matching
import glob  # For file pattern matching

chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

def getProfessors(course):
    print("Searching for professors who teach " + course + "...")
    start_time = time.time()  # Track start time for performance logging

    coursebookDriver = webdriver.Chrome(options = Options())  # Launch Chrome in headless mode
    coursebookDriver.get("https://coursebook.utdallas.edu/guidedsearch")  # Open the coursebook search page
    time.sleep(1)  # Allow the page to load
    coursebookDriver.find_element(By.XPATH, '//*[@id="tabset-menubar"]/div/div/ul/li[1]').click()  # Click on the appropriate tab

    time.sleep(1)
    courseBookSearch = coursebookDriver.find_element(By.XPATH, '//*[@id="srch"]')
    courseBookSearch.send_keys(course)  # Enter the course ID into the search bar
    time.sleep(1)  # Allow time for the page to load
    coursebookDriver.find_element(By.XPATH, '//*[@id="classsearch"]/button').click()  # Click the search button
    time.sleep(1)  # Allow the page to load search results
    Results = coursebookDriver.find_element(By.XPATH, '//*[@id="searchresults"]/b')  # Check for search results

    if("no items found" in Results.text):  # Handle case where no results are found
        print("No results found for " + course)
        return "error"
    
    table = coursebookDriver.find_element(By.XPATH, '//*[@id="sr"]/div/table').text  # Extract the table text containing professor info
    pattern = re.compile(r"\d+ (?:Credits|Semester Credit Hours)\) (?!-Staff-)([^\n]+)")  # Regex pattern to find professor names

    # Find all matches and remove duplicates
    professors = set(re.findall(pattern, table))  # Use a set to eliminate duplicate entries
    coursebookDriver.quit()  # Close the ChromeDriver session
    return professors  # Return the set of professor names

def main():
    start_t = time.time()  # Track start time for overall execution
    getProfessors("CS3345")  # Test the function with a specific course ID
    print("OVERALL: ")
    print(+ time.time() - start_t)  # Log the total time taken

if(__name__ == "__main__"):
    main()  # Execute the main function when the script is run directly

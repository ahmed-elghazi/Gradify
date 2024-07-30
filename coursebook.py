import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import glob

chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

def getProfessors(course):
    print("Searching for professors who teach " + course + "...")
    start_time = time.time()

    coursebookDriver = webdriver.Chrome(options = Options())
    coursebookDriver.get("https://coursebook.utdallas.edu/guidedsearch") #Open the website
    time.sleep(1)
    coursebookDriver.find_element(By.XPATH, '//*[@id="tabset-menubar"]/div/div/ul/li[1]').click() #wait for the page to load

    time.sleep(1)
    courseBookSearch = coursebookDriver.find_element(By.XPATH, '//*[@id="srch"]')
    courseBookSearch.send_keys(course) #enter course into search bar
    time.sleep(1) #let the page load
    coursebookDriver.find_element(By.XPATH, '//*[@id="classsearch"]/button').click() #search for the course
    time.sleep(1) #let the page load
    Results = coursebookDriver.find_element(By.XPATH, '//*[@id="searchresults"]/b') #check if results were found

    if("no items found" in Results.text):
        print("No results found for " + course)
        return "error"
    
    table = coursebookDriver.find_element(By.XPATH, '//*[@id="sr"]/div/table').text
    pattern = re.compile(r"\d+ (?:Credits|Semester Credit Hours)\) (?!-Staff-)([^\n]+)")

    # Find all matches and remove duplicates
    professors = set(re.findall(pattern, table))
    coursebookDriver.quit() #close the coursebook
    print(time.time() - start_time)
    return professors

def main():
    start_t = time.time()
    getProfessors("CS3345")
    print("OVERALL: ")
    print(+ time.time() - start_t)
if(__name__ == "__main__"):
    main()
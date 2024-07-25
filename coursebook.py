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
#chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
#driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\WebDrivers\chromedriver.exe')
    #driver = webdriver.Chrome(options=chrome_options)
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
#print(driver.execute_script("return navigator.userAgent;"))

# def getProfessors(course):
#     start_time = time.time()

#     coursebookDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
#     coursebookDriver.get("https://coursebook.utdallas.edu/search") #Open the website

#     time.sleep(0.5)
#     courseBookSearch = coursebookDriver.find_element(By.XPATH, '//*[@id="srch"]')
#     courseBookSearch.send_keys(course) #enter course into search bar
#     time.sleep(0.5) #let the page load
#     coursebookDriver.find_element(By.XPATH, '//*[@id="classsearch"]/button').click() #search for the course
#     time.sleep(0.5) #let the page load
#     Results = coursebookDriver.find_element(By.XPATH, '//*[@id="searchresults"]/b') #check if results were found

#     if("no items found" in Results.text):
#         print("No results found for " + course)
#         return None
    
#     table = coursebookDriver.find_element(By.XPATH, '//*[@id="sr"]/div/table').text

#     #read from page and put into dataframe table pandas something
#     pattern = r'\(\d+ Semester Credit Hours\) ((?!-Staff-).+?)\n' #get all profs except 'staff'
#     professors = set(re.findall(pattern, table)) #set to remove duplicates
#     coursebookDriver.quit() #close the coursebook
#     end_time = time.time()
#     execution_time = end_time - start_time
#     return professors

def getProfessors(course):
    print("Searching for professors who teach " + course + "...")
    start_time = time.time()

    coursebookDriver = webdriver.Chrome(options = Options())
    #coursebookDriver.get("https://coursebook.utdallas.edu/search/CS3345") #Open the website
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
        return None
    
    table = coursebookDriver.find_element(By.XPATH, '//*[@id="sr"]/div/table').text

    #read from page and put into dataframe table pandas something
    # pattern = r'\(\d+ Semester Credit Hours\) ((?!-Staff-).+?)\n' #get all profs except 'staff'
    # professors = set(re.findall(pattern, table)) #set to remove duplicates
    # Define the pattern to extract instructor names
    # pattern = r'\(4 Credits\) ((?!Staff)[A-Za-z ]+) Combined Lec/Lab'
    # pattern = r'\bCS \d+\.\d+\b.*?\)\s*(.+?)(?=\n\d{2}|\Z)'
    # pattern = re.compile(r"(?<=Semester Credit Hours\) )[^-\n]+(?=\n| -|$)")
    # pattern = re.compile(r"\d+ (?:Credits|Semester Credit Hours)\) ([^\n]+?) Combined Lec/Lab")
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
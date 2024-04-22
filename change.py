from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium import webdriver

import time
import logging
import openai

from webdriver_confi import webdriver_config
from dotenv import load_dotenv
import os

import glob


# Load environment variables from .env file
load_dotenv()

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY", "default_openai_api_key")

class LoomRequest(BaseModel):
    page_url: str
    # prompt: str

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# __________________________________________________________________
def login(driver):
    for _ in range(5):  # Try logging in 3 times
        try:
            driver.get("https://platform.fullcontact.com/login")
            emailAdd = "hello@onenine.com"
            password = "6uVX3M&1P5]48uN"
            # Find and fill email input
            email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-email"))
            )
            email_input.clear()
            time.sleep(1)  # Add a small delay before sending keys
            email_input.send_keys(emailAdd)

            # Find and fill password input
            password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > input"))
            )
            password_input.clear()
            time.sleep(1)  # Add a small delay before sending keys
            password_input.send_keys(password)

            # Click submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > button")
            submit_button.click()

            # Wait for successful login
            WebDriverWait(driver, 10).until(
                EC.url_contains("https://platform.fullcontact.com/developers/recognition/dashboard")  # Adjust this to the URL you expect after login
            )

            # If login successful, return True
            return True

        except TimeoutException:
            logging.error("Timeout: Login failed. Retrying.......")
            logging.error(KeyError)
            time.sleep(3)
            continue

    # If all attempts fail, return False
    return False



# Rest of your imports and code...

@app.post("/download_FullReport/")
async def download_FullReport(request: LoomRequest):
    data = []
    
    # Initialize the driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--disable-notifications")
    
    # Set download directory
    download_dir = os.path.join(os.getcwd(), "downloads")  # Change this path to your desired download directory
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)
    
    # Add these options to disable third-party cookies blocking
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-cookie-encryption")
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(options=options)
    
    wait = WebDriverWait(driver, 20)
    loginStatus = login(driver)
    logging.debug("_______________loginStatus")
    logging.debug(loginStatus)
    # Try logging in
    if not loginStatus:
        driver.quit()
        return {"error": "Failed to login after multiple attempts."}

    # driver.get(request.page_url)
    # logging.debug(f'Navigating to video URL: {request.page_url}')
    # time.sleep(10)
    # try:
    #     # Assuming these elements are present on the login page, locate them and interact with them directly
    #     businessEmail_input = driver.find_element(By.ID, "login-email")
    #     businessEmail_input.click()
    #     businessEmail_input.send_keys('hello@onenine.com')
    #     logging.debug("_______________________send businessEmail_input_________________________________")
    # except TimeoutException:
    #     logging.error("Timeout: businessEmail_input Element not found or not clickable.")
    #     driver.quit()
    #     return {"error": "businessEmail_input not found or not clickable."}
    
    # try:
    #     businessPassword_input = driver.find_element(By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > input")
    #     businessPassword_input.send_keys("6uVX3M&1P5]48uN")
        
    #     submitButton = driver.find_element(By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > button")
    #     submitButton.click()
    try:
        time.sleep(10)  # Add a delay to ensure the page loads properly
        ReportSection = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div[1]/div[2]/div/a[5]')))
        ReportSection = driver.find_element(By.CSS_SELECTOR, '#app > div > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(2) > div > a:nth-child(5)')
        ReportSection.click()
        
        time.sleep(10)  # Add a delay to ensure the page loads properly
        downloadFullReportButton = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/button')
        downloadFullReportButton.click()
        
        # Wait for the file to be downloaded
        time.sleep(10)
        
        # Find the downloaded file
        list_of_files = glob.glob(os.path.join(download_dir, "*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        
        # Read the file content as binary
        with open(latest_file, "rb") as file:
            file_content = file.read()
        
        # Return file content as binary data
        return file_content
        
    except TimeoutException:
        logging.error("Timeout: Element not found or not clickable.")
        driver.quit()
        return {"error": "Element not found or not clickable."}

    driver.quit()
































































































# # Rest of your imports and code...
# @app.post("/download_FullReport/")
# async def download_FullReport(request: LoomRequest):
#     data = []
    
#     # Initialize the driver
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)
#     options.add_argument("--window-size=1920,1200")
#     options.add_argument("--disable-notifications")
    
#     # Set download directory
#     download_dir = os.path.join(os.getcwd(), "downloads")  # Change this path to your desired download directory
#     if not os.path.exists(download_dir):
#         os.makedirs(download_dir)
#     prefs = {"download.default_directory": download_dir}
#     options.add_experimental_option("prefs", prefs)
    
#     # Add these options to disable third-party cookies blocking
#     options.add_argument("--disable-web-security")
#     options.add_argument("--disable-cookie-encryption")
#     options.add_argument('log-level=3')

#     driver = webdriver.Chrome(options=options)
    
#     wait = WebDriverWait(driver, 20)
    
#     driver.get(request.page_url)
#     logging.debug(f'Navigating to video URL: {request.page_url}')
#     time.sleep(10)
#     try:
#         # Assuming these elements are present on the login page, locate them and interact with them directly
#         businessEmail_input = driver.find_element(By.ID, "login-email")
#         businessEmail_input.click()
#         businessEmail_input.send_keys('hello@onenine.com')
#         logging.debug("_______________________send businessEmail_input_________________________________")
#     except TimeoutException:
#         logging.error("Timeout: businessEmail_input Element not found or not clickable.")
#         driver.quit()
#         return {"error": "businessEmail_input not found or not clickable."}
    
#     try:
#         businessPassword_input = driver.find_element(By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > input")
#         businessPassword_input.click()
#         businessPassword_input.send_keys("6uVX3M&1P5]48uN")
#         logging.debug("_______________________send businessPassword_input_________________________________")
#     except TimeoutException:
#         logging.error("Timeout: businessPassword_input Element not found or not clickable.")
#         driver.quit()
#         return {"error": "businessPassword_input not found or not clickable."}
    
#     try:
#         submitButton = driver.find_element(By.CSS_SELECTOR, "#app > div > div > div:nth-child(3) > form > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > button")
#         submitButton.click()
#     except TimeoutException:
#         logging.error("Timeout: submitButton Element not found or not clickable.")
#         driver.quit()
#         return {"error": "submitButton not found or not clickable."}
        
#     time.sleep(10)  # Add a delay to ensure the page loads properly
    
#     try:
#         ReportSection = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div[1]/div[2]/div/a[5]')
#         ReportSection.click()
#     except TimeoutException:
#         logging.error("Timeout: ReportSection Element not found or not clickable.")
#         driver.quit()
#         return {"error": "ReportSection not found or not clickable."}
        
#     time.sleep(10)  # Add a delay to ensure the page loads properly

#     try: 
#         downloadFullReportButton = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[1]/div/div/button')
#         downloadFullReportButton.click()
#     except TimeoutException:
#         logging.error("Timeout: downloadFullReportButton Element not found or not clickable.")
#         driver.quit()
#         return {"error": "downloadFullReportButton not found or not clickable."}
        
#     # Wait for the file to be downloaded
#     time.sleep(10)
    
#     # Find the downloaded file
#     list_of_files = glob.glob(os.path.join(download_dir, "*"))
#     latest_file = max(list_of_files, key=os.path.getctime)
    
#     # Read the file content as binary
#     with open(latest_file, "rb") as file:
#         file_content = file.read()
    
#     # Return file content as binary data
#     return file_content
    
#     driver.quit()
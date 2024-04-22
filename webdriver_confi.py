import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def webdriver_config():
    options = Options()
    options.headless = False
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--disable-notifications")
    chrome_prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
        }
    }
    options.experimental_options["prefs"] = chrome_prefs
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=options)
    # Changing the property of the navigator value for webdriver to undefined
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # options = uc.ChromeOptions()
    # options.add_argument("--use-fake-ui-for-media-stream")
    # options.add_argument("--window-size=1920x1080")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-setuid-sandbox")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-application-cache")
    # options.add_argument("--disable-setuid-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # driver = uc.Chrome(service_log_path=WEBDRIVER_LOG_PATH,use_subprocess=False,options=options,version_main=122)
    return driver
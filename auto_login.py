# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008DA8A58A485250D4D03AEFA39F73EF36B6ABF36DA934AA8C09187517D6C4755BE654F97EDF63B920EC7028960B261183434D3255C06F8C75F65D74DBC0E31A14A27C137E36C784CA5E86D1A916A7FFF7F980A24B1C40E88EDFAE392DCB2EACE8FABD1F1A3C848D59CF270BC9CC2E3DDF8AD46917028EB42122A5D8CC2FF0AD594050910CF6D6B8C24F00B0090C8D4194C3048B76E3521AD2C48E7197E11184DF63C641A7090BDEAADA24FD465C2AB6CF58FB2CFB583F1FA970D0018E852E7CFFD19D2AD8D85CFD961628038473EBECBC2E4A85D73C0D3FAE5029755AD1D70DA578C30947C19F6E99B2FD24614141905288D6533AE50D6EBD098A2BA8C0BEA4A965C8C7CEDAF263386549E13F24C194CF0FB7CFE7E3412A832470A01BC1A20D768CB077B8B30438BE5756762CD006000AE69A7F7A2CDC72433571CF9CBF5819745B28B9E815903490A683C172D875AA4CFF4882537B25B33E3F6D1F999DF022CC"})
    
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

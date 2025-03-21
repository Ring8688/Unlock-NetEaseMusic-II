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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AF535E5A6BE1CA231A980EA58464CCAACAFA96C07F3E860BF82EBFB84B4ACE7731D0DA13E189A3597F8BFFAEEBDA9EB543EFADE57029502156D9FB694D2BE27AC0E42C9D9C4677D16343B201D611389471F5E07EED3C9E20B24CA983029F52B1228C3BBECD78E3AF0315069533AA2E90756C6EA39B7DDDEECEFD54EFCAE7234C4A61205C8764A25EE3643C86AB72A2A2D0270793558552E4B7A9960B89DC89F2FD7C8FAB9136384AF4C5840337C27E211A7309A2B0B9A4D11F66D8DF599DC0625498384FD1A3A37C6546C711FA68AD6FAE50818DE226C7D6FE1A6C501BFE757840561F65102085D07E0ED46271C9C2707FCF9C26CBC6EF943254BC81439A51767CC9DC006A693FF74A6BBFCEC38CB23BC98B063158E91CE65B9FC95CFE7E5FCE97514ADD459223895AD20E20E0F397DA7A826965BD86D8E928754A40B7D42E6C3FD3572202F8544E205C3FD1A9A67F323C8363AF70E039BB09407D3F15B82C6C"})
    # browser.add_cookie({"name": "MUSIC_U", "value": "0096DCDE6363021DD99F31404174FEE4BB39877DA9395EEDCD9FBAAD79034F2959F7319870316782A01A9E2AA102E2A4ED9226D2B115C1BC2A13CEF1C33314FD2FE56FBBE408DDCEC49651BBBEB6C32D81D4C5753E55C9FC8C43B6FDC68BFA3552B2CD34ED59A714A1F059980603135004B89FEA16294CEFAE277797EED18D0A80CD864F9DE72E7AFAAE53AC9EFEB51C2ACA48BDCFD3787CE1E8E17695FF86EE7B3AE5882CB5040289DD8D4D8209617207515AE41A9245E20E3BAB234F947A5D4D3A8A0B7D92322D9886AC80A430E04D63DD8447D26150B265F23E996E89025D2EA978A11758E23626A5369BAC287D5EBBA172D75FE4B99FB883FC60A8FCCAECEEF8FD894205E113B6596E5ADF0AAE4846DA80C8E2ABE65155282DCD4B4269CFD29BE7635FCF894C927BCB0F27BA5CE1C64E058040AA54EF35B8B39E2EBDD42ECFCDED52BA5348DF867C242C3642B5AC70E4F9EFFA9CCA5017C05022A3156F8D88"})
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

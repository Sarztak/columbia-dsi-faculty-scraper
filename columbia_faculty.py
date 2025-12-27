from rich.traceback import install; install()
import json 
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

START_URL = "https://datascience.columbia.edu/people-type/faculty/" 
NEXT_BTN  = "//a[contains(@class,'next')]"
CARDS     = "//a[contains(@class,'group')]"
FIELDS = {
    "name":  "//h1[contains(@class,'font-bold')]",
    "dept":  "//dl[contains(@class,'mt-8')]",           # element, then .text
    "links": "//div[contains(@class,'border-t')]//a",   # elements, then .get_attribute('href')
    "info":  "//div[contains(@class,'gutenberg-editor')]//p"
}
OUT_FILE  = "dsi_faculty.json"

def wait(sel, xpath, timeout=5):
    return WebDriverWait(sel, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def wait_nxt_page(driver, nxt, timeout=5):
    return WebDriverWait(driver, timeout).until(EC.staleness_of(nxt))

def extract_one(driver, url):
    driver.get(url)
    wait(driver, FIELDS["name"])
    record = {}
    for key, xpath in FIELDS.items():
        try:
            if key == "links":
                # store the list of all links on the page
                record[key] = [
                    a.get_attribute("href") for a in driver.find_elements(By.XPATH, xpath)]
            elif key in ("name", "dept", "info"):
                # store other field as string
                el = driver.find_element(By.XPATH, xpath)
                record[key] = el.text
        except Exception as e:
            if key == "links":
                record[key] = {}
            elif key in ("name", "dept", "info"):
                record[key] = ""
            print(e)
    return record

def get_driver(binary_location=None, headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")

    # if binary is not provided, selenium will use the chrome binary in the 
    # standard install path
    if binary_location:
        options.binary_location = binary_location

    driver = webdriver.Chrome(options=options) 

    return driver


def main():
    # fetch the headless browser
    driver = get_driver(headless=True)

    # retrive the information and dump to txt file
    # get_info(browser, URL)

    data, page = [], 1
    driver.get(START_URL)
    while True:
        print(f"[page {page}]")
        wait(driver, CARDS) 
        cards = driver.find_elements(By.XPATH, CARDS)
        hrefs = [c.get_attribute("href") for c in cards] 

        current_page_url = driver.current_url
        for url in hrefs:
            data.append(extract_one(driver, url))

        driver.get(current_page_url) 
        try:
            nxt = driver.find_element(By.XPATH, NEXT_BTN)
            nxt.click()
            wait_nxt_page(driver, nxt) # wait for next page to load
            page += 1
        except Exception:
            break

    Path(OUT_FILE).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"saved {len(data)} records -> {OUT_FILE}")
    driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level='DEBUG')
    main()
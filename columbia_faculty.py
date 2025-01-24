from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from scrapy import Selector
import time
import logging


def get_browser():
    '''
    Function to start the browser in headless mode
    '''
    logging.info("Opening connection...") 
    driver_path = r".\chromedriver.exe"
    try:
        service = Service(driver_path)
        option = webdriver.ChromeOptions()
        option.add_argument("--headless=new")
    except Exception as e:
        logging.info('e')
    
    return webdriver.Chrome(service=service, options=option)

   
def get_info(browser, url):
    browser.get(url)
    time.sleep(5)
    new_selector = Selector(text=browser.page_source)
    with open('DSI Faculty.txt', "w", encoding="utf-8") as w:
        while next_page:=new_selector.xpath("//div[@class='pagination text-center']/a[@class='next page-numbers']/@href").get():
            for faculty in new_selector.xpath("//a[@class='inline-block group']/@href").getall():
                browser.get(faculty)
                time.sleep(5)
                info_selector = Selector(text=browser.page_source)
                
                # name of the faculty member
                name = info_selector.xpath("//h1[@class='font-bold type-preset-2']/text()").get() 
                
                # department of the faculty member
                dept = info_selector.xpath("//dl[@class='mt-8']//text()").getall()

                # link to personal page
                links = info_selector.xpath("//div[@class='border-t border-slate-100 text-blue-400']//a/@href").getall()

                # info to personal page
                info = info_selector.xpath("//div[@class='gutenberg-editor']/p/text()").getall() 


                w.write(f'{name}\n')
                for line in dept:
                    w.write(f"{line.strip()}\n")
                for link in links:
                    w.write(f'\n{link}')
                w.write('\n\n')
                for i in info:
                    w.write(f"{i}")
                w.write('\n\n\n==============================================================================================================================================\n\n\n')
            browser.get(next_page)
            time.sleep(5)
            print(next_page)
            break
            new_selector = Selector(text=browser.page_source)


def main():
    logging.info("Start")
    browser = get_browser()
    url = "https://datascience.columbia.edu/people-type/faculty/" 
    get_info(browser, url)

if __name__ == "__main__":
    logging.basicConfig(level='DEBUG')
    main()